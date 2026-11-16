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

    Args:
        text: The Bengali or English text to convert into speech.
        voice_choice: Voice option - 'Bangladeshi Female (Nabanita)', 'Bangladeshi Male (Pradeep)', 'Indian Bengali Female (Tanishaa)', or 'Indian Bengali Male (Bashkar)'.
        rate: Speech speed adjustment like '+0%', '+15%', or '-10%'.
    Returns:
        Path to the generated MP3 audio file.
    """
    voice_id = VOICES.get(voice_choice, "bn-BD-NabanitaNeural")
    return asyncio.run(_synth(text, voice_id, rate))

demo = gr.Interface(
    fn=generate_bengali_tts,
    inputs=[
        gr.Textbox(label="Text", lines=4),
        gr.Dropdown(choices=list(VOICES.keys()), value="Bangladeshi Female (Nabanita)", label="Voice"),
        gr.Textbox(value="+0%", label="Speed Rate"),
    ],
    outputs=gr.Audio(type="filepath", label="Generated MP3"),
    title="Unlimited Bengali Edge TTS MCP",
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, mcp_server=True)
