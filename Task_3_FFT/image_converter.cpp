#include "image_converter.h"

bool GetImageSize(const std::string& image_filename, int* dim_x, int* dim_y) {
    FILE* image_file = fopen(image_filename.c_str(), "r");
    
    if (image_file == 0){
        return false;
    }

    fseek(image_file, 0, SEEK_END);
    long len = ftell(image_file);
    std::cout << len << std::endl;
    fseek(image_file, 0, SEEK_SET);
    
    if (len < 24) {
        fclose(image_file);
        return false;
    }
    
    unsigned char buf[24]; 
    fread(buf, 1, 24, image_file);

    if (buf[0] == 0xFF && buf[1] == 0xD8 && buf[2] == 0xFF && 
        buf[3] == 0xE0 && buf[6] == 'J' && buf[7] == 'F' && 
        buf[8] == 'I' && buf[9] == 'F') { 
        long pos = 2;
        while (buf[2] == 0xFF) { 
            if (buf[3] == 0xC0 || buf[3] == 0xC1 || buf[3] == 0xC2 || 
                buf[3] == 0xC3 || buf[3] == 0xC9 || buf[3] == 0xCA || buf[3] == 0xCB) {
                break;
            }
            pos += 2 + (buf[4] << 8) + buf[5];
            if (pos + 12 > len) {
                break;
            }
            fseek(image_file, pos, SEEK_SET); 
            fread(buf + 2, 1, 12, image_file);
        }
    }

    fclose(image_file);

    if (buf[0] == 0xFF && buf[1] == 0xD8 && buf[2] == 0xFF) { 
        *dim_y = (buf[7] << 8) + buf[8];
        *dim_x = (buf[9] << 8) + buf[10];
        return true;
    }
    if (buf[0] == 'G' && buf[1] == 'I' && buf[2] == 'F'){ 
        *dim_x = buf[6] + (buf[7] << 8);
        *dim_y = buf[8] + (buf[9] << 8);
        return true;
    }
    if (buf[0] == 0x89 && buf[1] == 'P' && buf[2] == 'N' && 
        buf[3] == 'G' && buf[4] == 0x0D && buf[5] == 0x0A &&
        buf[6] == 0x1A && buf[7] == 0x0A && buf[12] == 'I' && 
        buf[13] == 'H' && buf[14] == 'D' && buf[15] == 'R') { 
        *dim_x = (buf[16] << 24) + (buf[17] << 16) + (buf[18] << 8) + (buf[19] << 0);
        *dim_y = (buf[20] << 24) + (buf[21] << 16) + (buf[22] << 8) + (buf[23] << 0);
        return true;
    }

    return false;
}

void ConvertImageToArray(const std::string& image_filename, const std::string& array_filename) {
    int dim_x = 1;
    int dim_y = 1;
    bool flag = GetImageSize(image_filename, &dim_x, &dim_y);
    if (flag) {
        std::cout << dim_x << " " << dim_y << std::endl;
    }
    else {
        std::cout << "False" << std::endl;
    }
    

    FILE* image_file = fopen(image_filename.c_str(), "r");
    FILE* array_file = fopen(array_filename.c_str(), "w");
    
    unsigned char data;
    char line_len = 0;

    fseek(image_file, 0, SEEK_SET);
    
    while (true) {
        if (feof(image_file)) {
            break;
        }
        data = getc(image_file);
        
        if (line_len >= 32) {
            line_len = 0;
            fprintf(array_file, "\n");
        }

        fprintf(array_file, "0x%02X ", data);
        line_len++;
    }

    fclose(image_file);
    fclose(array_file);
}

int main() {
    ConvertImageToArray("stinkbug.png", "array.txt");
    
    return 0;
}