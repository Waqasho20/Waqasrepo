from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import requests, os
from urllib.parse import urlparse

class DownloaderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.input = TextInput(hint_text='Paste Facebook/Instagram URL', multiline=False)
        self.label = Label(text="📥 Waiting...")
        button = Button(text="Start Download", on_press=self.download)

        layout.add_widget(self.input)
        layout.add_widget(button)
        layout.add_widget(self.label)
        return layout

    def download(self, instance):
        url = self.input.text.strip()
        if not url:
            self.label.text = "❌ Please enter a URL"
            return

        try:
            res = requests.post(
                "https://tera.backend.live/allinone",
                headers={
                    "x-api-key": "pxrAEVHPV2S0yczPyv9bE9n8JryVwJAw",
                    "content-type": "application/json"
                },
                json={"url": url}
            )
            data = res.json()
        except:
            self.label.text = "❌ Request failed"
            return

        # Check for video
        if "video" in data and data["video"]:
            v = data["video"][0]
            vurl = v.get("video") or v.get("url") if isinstance(v, dict) else v
            filename = os.path.basename(urlparse(vurl).path).split("?")[0]
            path = f"/sdcard/Download/{filename}"
            try:
                r = requests.get(vurl, stream=True)
                with open(path, "wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        f.write(chunk)
                self.label.text = f"✅ Saved: {path}"
            except:
                self.label.text = "❌ Failed to download video"

        elif "image" in data and data["image"]:
            for i, img_url in enumerate(data["image"], 1):
                ipath = f"/sdcard/Pictures/img_{i}.jpg"
                try:
                    r = requests.get(img_url)
                    with open(ipath, "wb") as f:
                        f.write(r.content)
                except:
                    self.label.text = f"⚠️ Image {i} failed"
            self.label.text = "✅ Images downloaded"
        else:
            self.label.text = "❌ No media found"

if __name__ == "__main__":
    DownloaderApp().run()
