#ifndef __STREAM_H__
#define __STREAM_H__


#include "common-sdl.h"
#include "common.h"
#include "whisper.h"

#include <cassert>
#include <cstdio>
#include <string>
#include <thread>
#include <vector>
#include <fstream>

struct whisper_params {
    int32_t n_threads  = std::min(4, (int32_t) std::thread::hardware_concurrency());
    int32_t step_ms    = 3000;
    int32_t length_ms  = 10000;
    int32_t keep_ms    = 200;
    int32_t capture_id = -1;
    int32_t max_tokens = 32;
    int32_t audio_ctx  = 0;

    float vad_thold    = 0.6f;
    float freq_thold   = 100.0f;

    bool speed_up      = false;
    bool translate     = false;
    bool no_fallback   = false;
    bool print_special = false;
    bool no_context    = true;
    bool no_timestamps = false;
    bool tinydiarize   = false;
    bool save_audio    = false; // save audio to wav file
    bool use_gpu       = true;

    std::string language  = "en";
    std::string model     = "models/ggml-base.en.bin";
    std::string fname_out;
};

void whisper_print_usage(int argc, char ** argv, const whisper_params & params);
std::string to_timestamp(int64_t t) ;
bool whisper_params_parse(int argc, char ** argv, whisper_params & params) ;


class STT_Whisper{

    private : 
        int n_samples_step ;
        int n_samples_len  ;
        int n_samples_keep ;
        int n_samples_30s  ;

        bool use_vad;

        int n_new_line;

        struct whisper_context_params cparams;

        struct whisper_context * ctx ;

        std::vector<float> pcmf32    ;
        std::vector<float> pcmf32_old;
        std::vector<float> pcmf32_new;

        std::vector<whisper_token> prompt_tokens;
        bool is_running = true;

        whisper_params params;

        wav_writer wavWriter;

        audio_async *audio;


        int n_iter = 0;

        std::ofstream fout;

    public:

    STT_Whisper(int nb, char ** argv);
    void kill_process ();
    void switch_run_true();
    char* run(int nb, char ** argv);
    int yes_or_no(int nb, char ** argv);
};

#endif