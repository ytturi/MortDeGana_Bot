from mamba import description, context, it, before
from os import listdir
from expects import expect, be_true, be_false

# Import from files in order to work with coverage
import importlib.util
spec = importlib.util.spec_from_file_location("meldebot.confs", "meldebot/confs.py")
confs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(confs)


with description('Configs manager'):
    with context('Init config file'):
        with before.each:
            self.fname = 'mortdegana.cfg'
        with it('creates "mortdegana.cfg" with no args'):
            files = [f for f in listdir() if f==self.fname]
            expect(self.fname in files).to(be_false)
            confs.init_configs()
            files = [f for f in listdir() if f==self.fname]
            expect(self.fname in files).to(be_true)

        with _it('creates config on custom path with args'):
            pass
