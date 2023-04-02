#pragma once

#include <iostream>
#include <stdio.h>
#include <fstream>

bool GetImageSize(const std::string& image_filename, int& dim_x, int& dim_y);
void ConvertImageToArray(const std::string& image_filename, const std::string& array_filename);