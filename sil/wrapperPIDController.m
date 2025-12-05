function [u, P, I, D] = wrapperPIDController(w, y, doParameterSync)

    persistent pid_obj;

    if nargin < 2
        doParameterSync = true;
    end
    
    %% Init
    if isempty(pid_obj)
        parentFolder = fullfile(pwd, '..');              
        py.sys.path().insert(int32(0), parentFolder); 
        mod = py.importlib.import_module('PIDController');
        mod = py.importlib.reload(mod);

        pid_obj = mod.PIDController();   
        pid_obj.reset();

        if doParameterSync

            kp = eval(get_param('foerderband_sil/Regler/kp', 'Gain'));
            Tn = 1/eval(get_param('foerderband_sil/Regler/1 durch Tn', 'Gain'));
            Tv = eval(get_param('foerderband_sil/Regler/Tv', 'Gain'));
        
            pid_obj.kp = kp * 1023/1000/5;
            pid_obj.Tn = Tn;
            pid_obj.Tv = Tv;

            disp pid_obj
        end
    end
    
    pid_obj.reference_value = w*1000;
    targetValue = pid_obj.calculate_controller_output(y*1000);
    P = double(targetValue{2}{1})*5.0/1023.0;
    I = double(targetValue{2}{2})*5.0/1023.0;
    D = double(targetValue{2}{3})*5.0/1023.0;

    u = P+I+D;
end
    