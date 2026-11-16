import asyncio
import os
import tempfile
import edge_tts
import gradio as gr

VOICES = {
    "Bangladeshi Female (Nabanita)": "bn-BD-NabanitaNeural",
    "Bangladeshi Male (Pradeep)": "bn-BD-PradeepNeural",
    "Indian Bengali Female (Tanishaa)": "bn-IN-TanishaaNeural",
    "Indian Bengali Male (Bashkar)": "bn-IN-BashkarNeural",
    "English US Male - Brian (calm storyteller)": "en-US-BrianMultilingualNeural",
    "English US Male - Andrew (warm, natural)": "en-US-AndrewMultilingualNeural",
    "English US Male - Guy (deeper, dramatic)": "en-US-GuyNeural",
    "English UK Male - Ryan (cinematic)": "en-GB-RyanNeural",
    "English US Female - Ava (natural)": "en-US-AvaMultilingualNeural",
    "English US Female - Emma (bright)": "en-US-EmmaMultilingualNeural",
}

async def _synth(text: str, voice_id: str, rate: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()
    communicate = edge_tts.Communicate(text=text, voice=voice_id, rate=rate)
    await communicate.save(tmp.name)
    return tmp.name

def generate_bengali_tts(
    text: str,
    voice_choice: str = "Bangladeshi Female (Nabanita)",
    rate: str = "+0%",
) -> str:
    """Convert Bengali or English text into a downloadable MP3 speech file using Microsoft Edge neural voices.

    Use a Bengali voice for Bengali text and an English voice for English text.

    Args:
        text: The Bengali or English text to convert into speech.
        voice_choice: Bengali voices: 'Bangladeshi Female (Nabanita)', 'Bangladeshi Male (Pradeep)', 'Indian Bengali Female (Tanishaa)', 'Indian Bengali Male (Bashkar)'. English voices: 'English US Male - Brian (calm storyteller)', 'English US Male - Andrew (warm, natural)', 'English US Male - Guy (deeper, dramatic)', 'English UK Male - Ryan (cinematic)', 'English US Female - Ava (natural)', 'English US Female - Emma (bright)'.
        rate: Speech speed adjustment like '+0%', '+15%', or '-10%'. For dramatic narration try '-8%'.
    Returns:
        Path to the generated MP3 audio file.
    """
    if voice_choice not in VOICES:
        raise ValueError(f"Unknown voice '{voice_choice}'. Choose one of: {', '.join(VOICES)}")
    return asyncio.run(_synth(text, VOICES[voice_choice], rate))

demo = gr.Interface(
    fn=generate_bengali_tts,
    inputs=[
        gr.Textbox(label="Text", lines=4),
        gr.Dropdown(choices=list(VOICES.keys()), value="Bangladeshi Female (Nabanita)", label="Voice"),
        gr.Textbox(value="+0%", label="Speed Rate"),
    ],
    outputs=gr.Audio(type="filepath", label="Generated MP3"),
    title="Unlimited Bengali + English Edge TTS MCP",
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, mcp_server=True)
