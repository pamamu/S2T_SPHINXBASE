import shutil
import subprocess
from os import path

from utils import IO


def generate_files_structure(info_json):
    """
    TODO DOCUMENTATION
    :param info_json:
    :return:
    """

    # GENERATE IDS AND TRANSCRIPTION FILES
    main_path = IO.get_tmp_main_folder()

    fileids_path = path.join(main_path, 'audios.fileids')
    transcription_path = path.join(main_path, 'audios.transcription')

    fileids = open(fileids_path, 'w')
    transcription = open(transcription_path, 'w')

    i = 0
    for audio in info_json:
        words = [words['text'] for voice in audio['voices'] for words in voice['trans']]
        if len(words) < 1:
            continue
        simple_audio_name = "audio_{}".format(i)
        audio_name = "{}.wav".format(simple_audio_name)
        shutil.copy(audio['path'], path.join(main_path, audio_name))
        # shutil.move(audio['path'], path.join(main_path, audio_name))
        sentence = " ".join(words)
        fileids.write(simple_audio_name + "\n")
        transcription.write(sentence + " ({})\n".format(simple_audio_name))
        i += 1

    fileids.close()
    transcription.close()

    return fileids_path, transcription_path


def convert_lm(origin_lm):
    """
    TODO DOCUMENTATION
    :param origin_lm:
    :return:
    """
    command = 'sphinx_lm_convert'
    out_path = path.join(IO.get_tmp_main_folder(), 'model.lm.bin')

    script = [command,
              '-i', origin_lm,
              '-o', out_path]
    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return out_path


def generate_aff(model_folder, fileids_path):
    """
    TODO DOCUMENTATION
    :return:
    """

    command = 'sphinx_fe'

    script = [command,
              '-argfile', path.join(model_folder, 'feat.params'),
              '-samprate', '16000',
              '-c', fileids_path,
              '-di', IO.get_tmp_main_folder(),
              '-do', IO.get_tmp_main_folder(),
              '-ei', 'wav',
              '-eo', 'mfc',
              '-mswav', 'yes'
              ]
    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return True


def convert_mdef(model_folder):
    """
    TODO DOCUMENTATION
    :return:
    """
    command = 'pocketsphinx_mdef_convert'
    in_path = path.join(model_folder, 'mdef')
    out_path = path.join(model_folder, 'mdef.txt')

    script = [command,
              '-text', in_path, out_path]
    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return out_path


def accumulate_obs_count():
    """
    todo documentation
    :return:
    """
    base = IO.get_sphinxtrain_folder()
    command = 'bw'

    script = [path.join(base, command),
              '-hmmdir', 'es',
              '-moddeffn', 'es/mdef.txt',
              '-ts2cbfn', '.ptm.',
              '-feat', '1s_c_d_dd',
              '-svspec', '0-12/13-25/26-38',
              '-cmn', 'current',
              '-agc', 'none',
              '-dictfn', 'es.dic',
              '-ctlfn', 'audios.fileids',
              '-lsnfn', 'audios.transcription',
              '-accumdir', path.basename(IO.get_counts_folder())
              ]

    p = subprocess.call(script, cwd=IO.get_tmp_main_folder())
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return True


def mllr_transformation(model_folder):
    """
    TODO DOCUMENTATION
    :return:
    """

    command = 'mllr_solve'

    out_file = path.join(IO.get_counts_folder(), 'mllr_matrix')

    script = [command,
              '-meanfn', path.join(model_folder, 'means'),
              '-varfn', path.join(model_folder, 'variances'),
              '-outmllrfn', out_file,
              '-accumdir', IO.get_counts_folder()
              ]

    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return out_file


def reduce_language_model(language_model_path, out_language_model_path):
    """
    TODO DOCUMENTATION
    :param language_model_path:
    :param out_language_model_path:
    :return:
    """
    command = 'sphinx_lm_convert'

    script = [command,
              '-i', language_model_path,
              '-o', out_language_model_path,
              ]

    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in language model reduction')

    return out_language_model_path


def map_transformation(model_folder):
    # map_adapt \
    # -moddeffn resources/model/es/mdef.txt \
    # -ts2cbfn .ptm. \
    # -meanfn resources/model/es/means \
    # -varfn resources/model/es/variances \
    # -mixwfn resources/model/es/mixture_weights \
    # -tmatfn resources/model/es/transition_matrices \
    # -accumdir resources/tmp/audios/counts \
    # -mapmeanfn resources/tmp/audios/es/means \
    # -mapvarfn resources/tmp/audios/es/variances \
    # -mapmixwfn resources/tmp/audios/es/mixture_weights \
    # -maptmatfn resources/tmp/audios/es/transition_matrices

    base = IO.get_sphinxtrain_folder()
    command = 'map_adapt'

    script = [path.join(base, command),
              '-moddeffn', path.join(IO.get_base_model_path(), 'mdef.txt'),
              '-ts2cbfn', '.ptm.',
              '-meanfn', path.join(IO.get_base_model_path(), 'means'),
              '-varfn', path.join(IO.get_base_model_path(), 'variances'),
              '-mixwfn', path.join(IO.get_base_model_path(), 'mixture_weights'),
              '-tmatfn', path.join(IO.get_base_model_path(), 'transition_matrices'),
              '-accumdir', IO.get_counts_folder(),
              '-mapmeanfn', path.join(model_folder, 'means'),
              '-mapvarfn', path.join(model_folder, 'variances'),
              '-mapmixwfn', path.join(model_folder, 'mixture_weights'),
              '-maptmatfn', path.join(model_folder, 'transition_matrices'),
              ]

    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return model_folder
