//
// Created by michael on 20/07/2024.
//

#include <iostream>
#include <filesystem>
#include <fstream>
#include <vector>
#include <thread>
#include <future>
#include <sstream>
#include <string>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-page.h>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <nlohmann/json.hpp>
#include <openai/openai.h>

namespace fs = std::filesystem;

class LoggerSetup {
public:
    static void setup_logging(const fs::path &summary_file_path) {
        std::ofstream(summary_file_path, std::ofstream::out).close(); // Clear the file
        auto logger = spdlog::basic_logger_mt("basic_logger", "logfile.log");
        spdlog::set_default_logger(logger);
        spdlog::set_level(spdlog::level::info);
    }

    static void log_error(const std::string &message) {
        spdlog::error(message);
    }

    static void log_info(const std::string &message) {
        spdlog::info(message);
    }
};
