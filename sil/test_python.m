%% TEST PYTHON
% Führt die vorbereitenden Test für die SIL-Übung durch:
%
% # ITEM1 Erstellt eine Instanz der Test-Klasse und führt die
% Methoden-Calls 'addValue' und 'reset' durch
% # ITEM2 Erstellt eine Instanz der PID-Klasse und testet die
% wrapper-Funktion mittels zwei Funktionsaufrufes (zwei wegen presistency)
% 
%
%
global test_passed
test_passed=true;
errors = {};
%% Test-Klasse
printTestTitle('Test-Klasse')

%% Python-Version
printTestItem('Python Umgebung        ')
pyInfo = pyenv;
try
    v = str2double(pyInfo.Version);
    if v>3.5 || (v<3.2&&v>=3.1)
        printTestItemResult('OK', pyInfo.Version)
    elseif v>=3
        printTestItemResult('WARNUNG', 'Python-Version nicht aktuell')
    else
        printTestItemResult('FEHLER', 'Python-Version zu alt. <a href="https://www.python.org/downloads/release/python-3120/">Download Python 3.12</a>')
    end
catch
    printTestItemResult('FEHLER', '<a href="https://www.python.org/downloads/release/python-3120/">Download Python 3.12</a>')
end

%% Erzeuge Objekt
printTestItem('Erzeuge Python-Objekt   ')
try
    test_obj = py.importlib.reload(py.importlib.import_module('Test')).Test();
    printTestItemResult('OK')
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end

%% Verwende Python-Objekt
%% update
printTestItem('Python-Objekt - update')
try
    value = test_obj.addValue(12.3);
    if value == 12.3
        printTestItemResult('OK')
    else
        printTestItemResult('FEHLER', ['falsches Resultat: ' num2str(value)])
    end
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end
%% reset
printTestItem('Python-Objekt - reset   ')
try
    test_obj.reset();
    value = test_obj.state;
    if value == 0
        printTestItemResult('OK')
    else
        printTestItemResult('FEHLER', ['falsches Resultat: ' num2str(value)])
    end
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end
%% parameter
printTestItem('Python-Objekt - parameter')
try
    param = test_obj.param;
    test_obj.param = 2;
    value = test_obj.addValue(12.3);
    if value == 12.3*2 
        if param == 1
            printTestItemResult('OK')
        else
            printTestItemResult('FEHLER', ['parameter nicht geschrieben: ' num2str(param)])
        end
    else
        printTestItemResult('FEHLER', ['falsches Resultat: ' num2str(value)])
    end
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end



printTestResult()

%% PID-Klasse
%% update
printTestTitle('PID-Wrapper')
printTestItem('PID-Wrapper - update  ')
clear wrapperPIDController
try
    [u, P, I, D] = wrapperPIDController(0.415, 0.415, false);
    [u, P, I, D] = wrapperPIDController(0.415, 0.415, false);
    if u == 0
        printTestItemResult('OK')
    else e
        printTestItemResult('FEHLER', ['falsches Resultat: ' num2str(value)])
    end
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end

%% precistency
printTestItem('PID-Wrapper - presistency')
clear wrapperPIDController
try
    [u1, P, I, D] = wrapperPIDController(0.01, 0, false);
    [u2, P, I, D] = wrapperPIDController(0.01, 0, false);
    [u3, P, I, D] = wrapperPIDController(0.01, 0, false);
    if u2<u3
         printTestItemResult('OK')
    else
        printTestItemResult('FEHLER')
    end
catch e
    printTestItemResult('FEHLER')
    errors{end+1} = e;
end

printTestResult()

for e=errors
    rethrow(e{1});
end


%% Hilfsfunktionen
function [] = printTestTitle(title)
    global test_passed
    fprintf('TEST ''%s'':\n', title)
    test_passed = true;
end

function [] = printTestResult()
    global test_passed
    if test_passed
        fprintf('\t--> Test-Resultat:\t \t\t[BESTANDEN]\n')
    else
        fprintf('\t--> Test-Resultat:\t \t\t[FEHLER]\n')
    end
end

function [] = printTestItem(text)
    fprintf('\t- %s\t...', text)
end

function [] = printTestItemResult(result, info)
    global test_passed
    if nargin<2
        info = "";
    end

    if strcmp(result, 'FEHLER')
        test_passed = false;
    end

    fprintf('\t[%s] %s\n', result, info)
end

