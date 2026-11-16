VIVADO ?= vivado
.PHONY: all
all: ps.xsa
ps.xsa: export.tcl
	$(VIVADO) -mode batch -source export.tcl -log export.log -journal export.jou
