import gradio as gr
import soundfile as sf
from pedalboard import (
    Chorus,
    Compressor,
    Gain,
    HighpassFilter,
    LadderFilter,
    Limiter,
    LowpassFilter,
    Pedalboard,
    Phaser,
    Reverb,
)
from pedalboard_native import Distortion

EFFECTS = [
    "Compressor",
    "Chorus",
    "Distortion",
    "Gain",
    "HighpassFilter",
    "LadderFilter",
    "Limiter",
    "LowpassFilter",
    "Phaser",
    "Reverb",
]

INPUTS = [
    gr.inputs.Audio(label="Audio", type="file"),
    gr.inputs.CheckboxGroup(EFFECTS, label="Effects"),
    gr.inputs.Slider(
        minimum=-50, maximum=40, default=-60, label="compressor_threshold_db"
    ),
    gr.inputs.Slider(minimum=1, maximum=25, default=1, label="compressor_ratio"),
    gr.inputs.Slider(minimum=0.0, maximum=1.0, default=0.0, label="chorus_rate_hz"),
    gr.inputs.Slider(minimum=0.0, maximum=1.0, default=0.0, label="chrous_depth"),
    gr.inputs.Slider(
        minimum=0.0, maximum=10.0, default=0.0, label="chorus_centre_delay_ms"
    ),
    gr.inputs.Slider(minimum=0.0, maximum=1.0, default=0.0, label="chorus_feedback"),
    gr.inputs.Slider(minimum=0.0, maximum=1.0, default=0.0, label="chorus_mix"),
    gr.inputs.Slider(minimum=1, maximum=25, default=1, label="drive_db"),
    gr.inputs.Slider(minimum=1, maximum=25, default=1, label="gain_db"),
    gr.inputs.Slider(
        minimum=0, maximum=12000, default=0, label="highpass_cutoff_frequency_hz"
    ),
    gr.inputs.Slider(
        minimum=0, maximum=12000, default=0, label="lowpass_cutoff_frequency_hz"
    ),
    gr.inputs.Slider(
        minimum=0, maximum=12000, default=0, label="ladder_filter_cutoff_hz"
    ),
]


def effect(
    audio,
    checkbox,
    compressor_threshold_db,
    compressor_ratio,
    chorus_rate_hz,
    chorus_depth,
    chorus_centre_delay_ms,
    chorus_feedback,
    chorus_mix,
    drive_db,
    gain_db,
    highpass_cutoff_frequency_hz,
    lowpass_cutoff_frequency_hz,
    ladder_filter_cutoff_hz,
):

    audio, sr = sf.read(audio.name)

    # initialize empty pedalboard
    board = Pedalboard([], sample_rate=sr)

    # add the effects
    for checked in checkbox:
        if checked == "Compressor":
            board.append(
                Compressor(
                    threshold_db=compressor_threshold_db,
                    ratio=compressor_ratio,
                )
            )
        if checked == "Chorus":
            board.append(
                Chorus(
                    rate_hz=chorus_rate_hz,
                    depth=chorus_depth,
                    centre_delay_ms=chorus_centre_delay_ms,
                    feedback=chorus_feedback,
                    mix=chorus_mix,
                )
            )
        if checked == "Distortion":
            board.append(Distortion(drive_db=drive_db))
        if checked == "Gain":
            board.append(Gain(gain_db=gain_db))
        if checked == "HighpassFilter":
            board.append(
                HighpassFilter(cutoff_frequency_hz=highpass_cutoff_frequency_hz)
            )
        if checked == "LadderFilter":
            board.append(
                LadderFilter(
                    mode=LadderFilter.Mode.HPF12,
                    cutoff_hz=ladder_filter_cutoff_hz,
                )
            )
        if checked == "Limiter":
            board.append(Limiter())
        if checked == "LowpassFilter":
            board.append(LowpassFilter(cutoff_frequency_hz=lowpass_cutoff_frequency_hz))
        if checked == "Phaser":
            board.append(Phaser())
        if checked == "Reverb":
            board.append(Reverb())

    effected = board(audio)

    sf.write("output.wav", effected, sr)

    return "output.wav"


interface = gr.Interface(
    effect,
    inputs=INPUTS,
    outputs=gr.outputs.Audio(type="file"),
)
interface.launch(debug=True)
