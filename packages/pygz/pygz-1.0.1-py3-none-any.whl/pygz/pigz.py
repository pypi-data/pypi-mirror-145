import subprocess

class PigzFile(object):
    def __init__(self, path, mode="rt", threads=4):
        self.path = path
        self.mode = mode
        self.threads = threads
        self._process = None
        self._fw = None
        
        if self.mode == "rt":
            args = ["pigz", "-d", "-c", "-p", str(self.threads), self.path]
            self._process = subprocess.Popen(args, 
                                            stdout=subprocess.PIPE,
                                            encoding="utf-8")
        elif self.mode == "wt":
            args = ["pigz", "-p", str(self.threads), "-c"]
            self._fw = open(self.path, "w+")
            self._process = subprocess.Popen(args, 
                                            stdout=self._fw,
                                            stdin=subprocess.PIPE,
                                            encoding="utf-8")
        else:
            raise RuntimeError("Mode must be wt or rt.")
        
    def __iter__(self):
        assert self.mode == "rt"
        for line in self._process.stdout:
            yield line
        self._process.wait()
        assert self._process.returncode == 0
        self._process.stdout.close()
        self._process = None
        
    def write(self, line):
        assert self.mode == "wt"
        self._process.stdin.write(line)
    
    def close(self): 
        if self._process:
            if self.mode == "rt":
                self._process.kill()
                self._process.stdout.close()
                self._process = None
            elif self.mode == "wt":
                self._process.stdin.close()
                self._process.wait()
                self._process = None
                self._fw.close()
                self._fw = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    