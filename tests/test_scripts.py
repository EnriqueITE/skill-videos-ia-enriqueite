"""Pruebas locales: python -m unittest discover -s tests -v"""
import datetime
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "videos-ia-enriqueite" / "scripts"


class ScriptsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / name), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8")

    def project(self):
        result = self.run_script("nuevo_video.py", "--tema", "prueba", "--formato", "reel", "--raiz", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.root / (datetime.date.today().isoformat() + "_prueba_reel")

    def test_existing_project_preserves_work(self):
        base = self.project()
        script = base / "01_guion" / "guion.md"
        script.write_text("Mi guion editado", encoding="utf-8")
        result = self.run_script("nuevo_video.py", "--tema", "prueba", "--formato", "reel", "--raiz", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(script.read_text(encoding="utf-8"), "Mi guion editado")

    def test_empty_topic_rejected(self):
        result = self.run_script("nuevo_video.py", "--tema", "!!!", "--formato", "reel", "--raiz", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Requiere FFmpeg y FFprobe")
    def test_render_formats_and_short_audio(self):
        base = self.project()
        scenes = [{"inicio": 0, "fin": 2, "texto_pantalla": "Prueba visible", "iconos": ["check"]}]
        (base / "03_visual" / "escenas.json").write_text(json.dumps(scenes), encoding="utf-8")
        for formato in ("reel", "youtube"):
            with self.subTest(formato=formato):
                if formato == "youtube":
                    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                                    "sine=frequency=440:duration=0.5", str(base / "02_audio" / "locucion.wav")], check=True)
                output = self.root / (formato + ".mp4")
                result = self.run_script("montar_video.py", "--formato", formato, "--entrada", base,
                                         "--salida", output, "--escala", "0.1")
                self.assertEqual(result.returncode, 0, result.stderr)
                probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                        "-of", "json", str(output)], capture_output=True, text=True, check=True)
                data = json.loads(probe.stdout)
                self.assertAlmostEqual(float(data["format"]["duration"]), 2, delta=0.15)
                video = next(s for s in data["streams"] if s["codec_type"] == "video")
                self.assertEqual((video["width"], video["height"]), (108, 192) if formato == "reel" else (192, 108))
                self.assertTrue(any(s["codec_type"] == "audio" for s in data["streams"]))
                before = output.read_bytes()
                repeat = self.run_script("montar_video.py", "--formato", formato, "--entrada", base, "--salida", output)
                self.assertNotEqual(repeat.returncode, 0)
                self.assertEqual(before, output.read_bytes())

    @unittest.skipUnless(shutil.which("ffmpeg"), "Requiere FFmpeg")
    def test_invalid_scene_timing_rejected(self):
        base = self.project()
        for scenes in ([], [{"inicio": 1, "fin": 2}], [{"inicio": 0, "fin": -1}],
                       [{"inicio": 0, "fin": 2}, {"inicio": 1, "fin": 3}]):
            with self.subTest(scenes=scenes):
                (base / "03_visual" / "escenas.json").write_text(json.dumps(scenes), encoding="utf-8")
                output = self.root / "invalid.mp4"
                result = self.run_script("montar_video.py", "--formato", "reel", "--entrada", base, "--salida", output)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_hook_visible_first_frame(self):
        from PIL import ImageChops
        spec = importlib.util.spec_from_file_location("montar_video", SCRIPTS / "montar_video.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        mont = module.Montador("reel", str(self.root), escala=0.2)
        scene = {"inicio": 0, "fin": 3, "texto_pantalla": "Gancho visible"}
        hook = mont.fotograma(scene, 0, [])
        background = mont.fotograma({"inicio": 0, "fin": 3}, 0, [])
        self.assertIsNotNone(ImageChops.difference(hook, background).getbbox())


if __name__ == "__main__":
    unittest.main()
