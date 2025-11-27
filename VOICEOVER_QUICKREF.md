# Quick Reference: Manim Voiceover with SoX

## Installation
```powershell
pip install manim-voiceover[gtts]
```

## Basic Usage
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MyScene(VoiceoverScene):
    def construct(self):
        # Setup voice
        self.set_speech_service(GTTSService())
        
        # Use voiceover
        with self.voiceover(text="Hello world"):
            circle = Circle()
            self.play(Create(circle))
```

## With SoX Effects
```python
self.set_speech_service(
    GTTSService(
        lang="en",
        sox_effects=["pitch", "100", "tempo", "1.1", "treble", "3"]
    )
)
```

## Voice Presets (voiceover_backend.py)
- `teaching_assistant`: Friendly, energetic
- `professor`: Authoritative, calm
- `enthusiastic`: Very cheerful
- `calm`: Soothing, relaxed
- `neutral`: Standard voice

## Common SoX Effects
- `["pitch", "100"]` - Higher pitch (lighter voice)
- `["tempo", "1.1"]` - 10% faster
- `["treble", "3"]` - Clearer voice
- `["bass", "3"]` - Deeper voice
- `["reverb", "20"]` - Room echo

## Run Example
```powershell
manim -pql assistant_intro.py AssistantIntro
```

## Check SoX Installation
```powershell
python check_sox.py
```

## Full Documentation
See: VOICEOVER_GUIDE.md
