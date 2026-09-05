"""inc17: two test premises corrected (the tests were wrong, not the code)."""
import pathlib

p = pathlib.Path("tests/test_components.py")
s = p.read_text(encoding="utf-8")

a = '    lit = [r for r in out if plain(r).strip(NA.ON) == ""]'
b = '    lit = [r for r in out if plain(r) and plain(r).strip(NA.ON) == ""]'
assert s.count(a) == 1
s = s.replace(a, b)

start = s.index('    k = LG.kit("blueprint")\n    k.meter(3, 9')
end = s.index("k.mood)), stamp") + len("k.mood)), stamp")
new = '''    k = LG.kit("blueprint")
    # THE KNOCKOUT FIRES ON `alert` ALONE — a sheet with nothing overdue
    # carries no reversed cell and still states its condition (`_state_cell`).
    # That is also why ruling 10's move is cheap: on a calm sheet the single
    # knockout is UNSPENT, so a confirm may take it and the title block loses
    # nothing.
    k.mood = "alert"
    k.meter(3, 9, [1, 1, 1], 60)          # the block reads its figures here
    state, knocked = k._state_cell()
    assert knocked, "the alert mood is what spends the knockout"
    assert k.knockout_cell(state) in k.tabs(["board", "log"], "board")'''
s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8")
print("premises corrected")
