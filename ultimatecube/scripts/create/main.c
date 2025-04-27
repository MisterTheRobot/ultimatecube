#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h> // For usleep (use Sleep on Windows)
#include <windows.h>

#include <sys/stat.h> // For creating directories
#include <sys/types.h> // For creating directories

#include <direct.h> // For _mkdir on Windows

#define WIDTH 40
#define HEIGHT 40
#define PI 3.14159265358979323846

void setTextColor(int color);

char buffer[HEIGHT][WIDTH];
float zBuffer[HEIGHT][WIDTH];
float rotatedVertices[8][3];
float cubeVertices[8][3] = {
    {-1, -1, -1}, {1, -1, -1}, {1, 1, -1}, {-1, 1, -1},
    {-1, -1, 1},  {1, -1, 1},  {1, 1, 1},  {-1, 1, 1}
};
int cubeEdges[12][2] = {
    {0, 1}, {1, 2}, {2, 3}, {3, 0},
    {4, 5}, {5, 6}, {6, 7}, {7, 4},
    {0, 4}, {1, 5}, {2, 6}, {3, 7}
};

void lockConsoleWindowSize() {
    HWND consoleWindow = GetConsoleWindow();

    LONG style = GetWindowLong(consoleWindow, GWL_STYLE);
    SetWindowLong(consoleWindow, GWL_STYLE, style & ~WS_SIZEBOX & ~WS_MAXIMIZEBOX);

    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD bufferSize = {WIDTH, HEIGHT};
    SetConsoleScreenBufferSize(hOut, bufferSize);

    SMALL_RECT windowSize = {0, 0, WIDTH - 1, HEIGHT - 1};
    SetConsoleWindowInfo(hOut, TRUE, &windowSize);

    CONSOLE_FONT_INFOEX fontInfo = {0};
    fontInfo.cbSize = sizeof(fontInfo);
    fontInfo.dwFontSize.X = 10;
    fontInfo.dwFontSize.Y = 10;
    fontInfo.FontFamily = FF_DONTCARE;
    fontInfo.FontWeight = FW_NORMAL;
    wcscpy(fontInfo.FaceName, L"Consolas");
    SetCurrentConsoleFontEx(hOut, FALSE, &fontInfo);

    system("cls");
}

void clearBuffer() {
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            buffer[i][j] = ' ';
            zBuffer[i][j] = -INFINITY;
        }
    }
}

void drawPoint(int x, int y, float z, char c) {
    if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT) {
        if (z > zBuffer[y][x]) {
            zBuffer[y][x] = z;
            buffer[y][x] = c;
        }
    }
}

void drawLine(float x1, float y1, float z1, float x2, float y2, float z2, char c) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    float dz = z2 - z1;
    int steps = (int)(fmax(fabs(dx), fabs(dy)) * 2);

    for (int i = 0; i <= steps; i++) {
        float t = (float)i / steps;
        float x = x1 + t * dx;
        float y = y1 + t * dy;
        float z = z1 + t * dz;
        drawPoint((int)round(x), (int)round(y), z, c);
    }
}

void setTextColor(int color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}

void renderBuffer(int frameNumber) {
    printf("\033[H");
    int color = (frameNumber % 15) + 1;
    setTextColor(color);
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            putchar(buffer[i][j]);
        }
        putchar('\n');
    }
    setTextColor(color);
}

void rotateCube(float angleX, float angleY, float angleZ) {
    clearBuffer();

    float sinX = sin(angleX), cosX = cos(angleX);
    float sinY = sin(angleY), cosY = cos(angleY);
    float sinZ = sin(angleZ), cosZ = cos(angleZ);

    for (int i = 0; i < 8; i++) {
        float x = cubeVertices[i][0];
        float y = cubeVertices[i][1];
        float z = cubeVertices[i][2];

        float y1 = cosX * y - sinX * z;
        float z1 = sinX * y + cosX * z;

        float x2 = cosY * x + sinY * z1;
        float z2 = -sinY * x + cosY * z1;

        float x3 = cosZ * x2 - sinZ * y1;
        float y3 = sinZ * x2 + cosZ * y1;

        rotatedVertices[i][0] = x3;
        rotatedVertices[i][1] = y3;
        rotatedVertices[i][2] = z2;
    }

    for (int i = 0; i < 12; i++) {
        int v1 = cubeEdges[i][0];
        int v2 = cubeEdges[i][1];

        float x1 = rotatedVertices[v1][0] * 8 + WIDTH / 2;
        float y1 = rotatedVertices[v1][1] * 4 + HEIGHT / 2;
        float z1 = rotatedVertices[v1][2];

        float x2 = rotatedVertices[v2][0] * 8 + WIDTH / 2;
        float y2 = rotatedVertices[v2][1] * 4 + HEIGHT / 2;
        float z2 = rotatedVertices[v2][2];

        drawLine(x1, y1, z1, x2, y2, z2, 'O');
    }
}

void saveFrame(int frameNumber) {
    struct stat st = {0};
    char frames_dir[100];
    sprintf(frames_dir, "../frames"); // Adjusted to point to the parent folder

    if (stat(frames_dir, &st) == -1) {
        _mkdir(frames_dir);
    }

    char filename[100];
    sprintf(filename, "../frames/frame_%04d.txt", frameNumber); // Adjusted to point to the parent folder

    FILE *file = fopen(filename, "w");
    if (file) {
        for (int i = 0; i < HEIGHT; i++) {
            for (int j = 0; j < WIDTH; j++) {
                char c = buffer[i][j];
                fputc(c ? c : ' ', file);
            }
            fputc('\n', file);
        }
        fclose(file);
    } else {
        printf("Error: Could not create file %s\n", filename);
    }
}

int main() {
    lockConsoleWindowSize();

    printf("\033[2J");
    float angleX = 0, angleY = 0, angleZ = 0;
    int frameNumber = 0;

    while (frameNumber < 300) {
        rotateCube(angleX, angleY, angleZ);
        renderBuffer(frameNumber);
        saveFrame(frameNumber);
        angleX += 0.05;
        angleY += 0.03;
        angleZ += 0.02;
        usleep(30000);
        frameNumber++;
    }

    return 0;
}