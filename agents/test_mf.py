from mftool import Mftool

mf = Mftool()

scheme_code = "148989"

data = mf.get_scheme_quote(scheme_code)

print(data)