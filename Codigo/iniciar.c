#include <windows.h>
#include <shellapi.h>
#include "interfaz.inc"

void iniciar(void) {
    WCHAR ruta[MAX_PATH], dir[MAX_PATH];
    DWORD longitud = GetTempPathW(MAX_PATH, dir);
    if (longitud && longitud + 35 < MAX_PATH) {
        lstrcpyW(ruta, dir);
        lstrcatW(ruta, L"UAA_Fourier_");
        WCHAR token[17];
        wsprintfW(token, L"%08lx%08lx", GetCurrentProcessId(), GetTickCount());
        lstrcatW(ruta, token);
        lstrcatW(ruta, L".html");
        HANDLE f = CreateFileW(ruta, GENERIC_WRITE, 0, NULL, CREATE_NEW,
                               FILE_ATTRIBUTE_NORMAL, NULL);
        if (f != INVALID_HANDLE_VALUE) {
            DWORD escritos = 0;
            BOOL ok = WriteFile(f, pagina, sizeof(pagina)-1, &escritos, NULL);
            CloseHandle(f);
            if (ok && escritos == sizeof(pagina)-1 &&
                (INT_PTR)ShellExecuteW(NULL, L"open", ruta, NULL, NULL, SW_SHOWNORMAL) > 32)
                ExitProcess(0);
            DeleteFileW(ruta);
        }
    }
    MessageBoxW(NULL, L"No se pudo abrir la interfaz. Revise su navegador predeterminado y la carpeta temporal.",
                L"Laboratorio Fourier", MB_ICONERROR);
    ExitProcess(1);
}
