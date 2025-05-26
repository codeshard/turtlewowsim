from _example_imports import *

mages = []
num_trinkets = 9

base_sp = 1000
base_crit = 40
base_hit = 14

fm = Mage(
    name="nothing",
    sp=base_sp,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="scythe",
    sp=base_sp + 40,
    crit=base_crit + 2,
    hit=base_hit + 2,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="reos",
    sp=base_sp + 40,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages(reos=5))
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="eye of dim",
    sp=base_sp,
    crit=base_crit + 3,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="gulch",
    sp=base_sp + 30,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(endless_gulch=True),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="tear",
    sp=base_sp + 44,
    crit=base_crit,
    hit=base_hit + 2,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="toep",
    sp=base_sp,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages(toep=5))
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="mqg",
    sp=base_sp,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages(mqg=5))
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="mark of champ",
    sp=base_sp + 85,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="shard of nightmare",
    sp=base_sp + 36,
    crit=base_crit,
    hit=base_hit + 1,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages())
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()

fm = Mage(
    name="zandalarian hero charm",
    sp=base_sp,
    crit=base_crit,
    hit=base_hit,
    tal=FireMageTalents,
    opts=MageOptions(),
    equipped_items=EquippedItems(),
)
fm.smart_scorch(cds=CooldownUsages(zhc=5))
sim = Simulation(characters=[fm])
sim.run(iterations=20000, duration=300, print_casts=False)
sim.detailed_report()
