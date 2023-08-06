// Copyright (C) 2021 Matthias Nadig


#define PY_SSIZE_T_CLEAN

// C++ Extension for Python
// This header must always be included as the first one.
#include <Python.h>


#ifdef _WIN32

#include <windows.h>
#include <iostream>


// Flag that is set, in case std-handle could be acquired on the input etc.
// In PyCharm for example the GetStdHandle-function will return an error.
bool isOutModeSaved = true;
bool isInModeSaved = true;

DWORD dwOriginalOutMode = 0;
DWORD dwOriginalInMode = 0;

PyObject *activate(PyObject *self, PyObject *args) {
    // std::cout << "Activate" << std::endl;

    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE);

    if (hOut == INVALID_HANDLE_VALUE) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get output handle");
        isOutModeSaved = false;
        Py_RETURN_NONE;
    }
    if (hIn == INVALID_HANDLE_VALUE) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get input handle");
        isInModeSaved = false;
        Py_RETURN_NONE;
    }

    // Get to original
    if (!GetConsoleMode(hOut, &dwOriginalOutMode)) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get output mode");
        isOutModeSaved = false;
        Py_RETURN_NONE;
    }
    if (!GetConsoleMode(hIn, &dwOriginalInMode)) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get input mode");
        isInModeSaved = false;
        Py_RETURN_NONE;
    }

    DWORD dwRequestedOutModes = ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN;
    DWORD dwRequestedInModes = ENABLE_VIRTUAL_TERMINAL_INPUT;

    DWORD dwOutMode = dwOriginalOutMode | dwRequestedOutModes;
    DWORD dwInMode = dwOriginalInMode | ENABLE_VIRTUAL_TERMINAL_INPUT;

    // Activate ANSI escape codes
    if (!SetConsoleMode(hOut, dwOutMode)) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not set output console mode");
        isOutModeSaved = false;
        Py_RETURN_NONE;
    }

    if (!SetConsoleMode(hIn, dwInMode)) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not set input console mode");
        isInModeSaved = false;
        Py_RETURN_NONE;
    }

    Py_RETURN_NONE;
}


PyObject *deactivate(PyObject *self, PyObject *args) {
    // std::cout << "Deactivate" << std::endl;

    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE);

    if (hOut == INVALID_HANDLE_VALUE) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get output handle");
        Py_RETURN_NONE;
    }
    if (hIn == INVALID_HANDLE_VALUE) {
        // PyErr_SetString(PyExc_RuntimeError, "Could not get input handle");
        Py_RETURN_NONE;
    }
    
    // Reset to original
    if (isOutModeSaved) {
        if (!SetConsoleMode(hOut, dwOriginalOutMode)) {
            // PyErr_SetString(PyExc_RuntimeError, "Could not reset output console mode");
            Py_RETURN_NONE;
        }
    }
    if (isInModeSaved) {
        if (!SetConsoleMode(hIn, dwOriginalInMode)) {
            // PyErr_SetString(PyExc_RuntimeError, "Could not reset input console mode");
            Py_RETURN_NONE;
        }
    }

    Py_RETURN_NONE;
}

#endif


//====================================================================
//		Initialization functions for C++ Extension in Python
//====================================================================


static PyMethodDef methods[] = {
	/*
	| Function name exposed to Python	| C++ function name								| Input args					| Descr.|	*/
#ifdef _WIN32
	{ "activate_esc",                   (PyCFunction)activate,					        METH_VARARGS,					nullptr },
	{ "deactivate_esc",	                (PyCFunction)deactivate,					    METH_VARARGS,					nullptr },
#endif

	// Terminate the array with an object containing nulls
	{ nullptr, nullptr, 0, nullptr },
};

static PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"_windows",
	"no description",
	0,
	methods
};

PyMODINIT_FUNC PyInit__windows() {
	return PyModule_Create(&module);
}

