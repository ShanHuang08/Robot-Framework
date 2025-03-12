import subprocess, time

class Cmd_Runner():
    def Cur_Dir(self):
        """Return current directory in windows"""
        output = subprocess.run('cd', shell=True, capture_output=True, text=True)
        return output.stdout

    def Run_cmd(self, cmd, data_in=None, timeout=10):
        cmd_list = cmd.split(' ')
        # print(cmd_list)
        try:
            output = subprocess.run(cmd_list, capture_output=True, text=True, input=data_in, timeout=timeout)
            
            if output.stderr:
                print(f"Return code: {output.returncode}\nError: {output.stderr}")
            return output
        except FileNotFoundError as e:
            print(f"Error: {e}\n{cmd} is invalid")
        except subprocess.TimeoutExpired:
            print(f"Error: Command '{cmd}' timed out after {timeout} seconds.")

    def Popen_cmd(self, cmd, *data_in, timeout=10):
        """`Popen()` supports input mutiple times

        return **process.returncode**, **stdout**/**stderr**"""
        try:
            cmd_list = cmd.split(' ')
            process = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # print(process) #<Popen: returncode: None args: ['ping']>
            if data_in:
                for data in data_in:
                    process.stdin.write(data)
                    process.stdin.flush() # Make sure input value deliver immediatelly
                    time.sleep(0.5)

            process.stdin.close()
            
            stdout, stderr = process.communicate(timeout=timeout)

            if stderr: 
                print(f"Return code: {process.returncode}\nError: {stderr}")
                return process.returncode, stderr
            else:
                print(f"Return code: {process.returncode}\nOutput: {stdout}")
                return process.returncode, stdout
        except FileNotFoundError as e:
            print(f"Error: {e}\n{cmd} is invalid")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Error: Command '{cmd}' timed out after {timeout} seconds.")


    def Check_call(self, cmd):
        """Check cmd can be executed
        
        Return `0 (True)` or `1 (False)`"""
        try:
            cmd = cmd.split(' ')
            subprocess.check_call(
                    cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

