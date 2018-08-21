#!/usr/bin/env python
"""

Copyright (c) 2018 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from myhdl import *
import os

import axi

module = 'axi_adapter'
testbench = 'test_%s_32_32' % module

srcs = []

srcs.append("../rtl/%s.v" % module)
srcs.append("../rtl/axi_adapter_rd.v")
srcs.append("../rtl/axi_adapter_wr.v")
srcs.append("%s.v" % testbench)

src = ' '.join(srcs)

build_cmd = "iverilog -o %s.vvp %s" % (testbench, src)

def bench():

    # Parameters
    ADDR_WIDTH = 16
    S_DATA_WIDTH = 32
    S_STRB_WIDTH = (S_DATA_WIDTH/8)
    M_DATA_WIDTH = 32
    M_STRB_WIDTH = (M_DATA_WIDTH/8)
    ID_WIDTH = 8
    AWUSER_ENABLE = 0
    AWUSER_WIDTH = 1
    WUSER_ENABLE = 0
    WUSER_WIDTH = 1
    BUSER_ENABLE = 0
    BUSER_WIDTH = 1
    ARUSER_ENABLE = 0
    ARUSER_WIDTH = 1
    RUSER_ENABLE = 0
    RUSER_WIDTH = 1
    CONVERT_BURST = 1

    # Inputs
    clk = Signal(bool(0))
    rst = Signal(bool(0))
    current_test = Signal(intbv(0)[8:])

    s_axi_awid = Signal(intbv(0)[ID_WIDTH:])
    s_axi_awaddr = Signal(intbv(0)[ADDR_WIDTH:])
    s_axi_awlen = Signal(intbv(0)[8:])
    s_axi_awsize = Signal(intbv(0)[3:])
    s_axi_awburst = Signal(intbv(0)[2:])
    s_axi_awlock = Signal(bool(0))
    s_axi_awcache = Signal(intbv(0)[4:])
    s_axi_awprot = Signal(intbv(0)[3:])
    s_axi_awqos = Signal(intbv(0)[4:])
    s_axi_awregion = Signal(intbv(0)[4:])
    s_axi_awuser = Signal(intbv(0)[AWUSER_WIDTH:])
    s_axi_awvalid = Signal(bool(0))
    s_axi_wdata = Signal(intbv(0)[S_DATA_WIDTH:])
    s_axi_wstrb = Signal(intbv(0)[S_STRB_WIDTH:])
    s_axi_wlast = Signal(bool(0))
    s_axi_wuser = Signal(intbv(0)[WUSER_WIDTH:])
    s_axi_wvalid = Signal(bool(0))
    s_axi_bready = Signal(bool(0))
    s_axi_arid = Signal(intbv(0)[ID_WIDTH:])
    s_axi_araddr = Signal(intbv(0)[ADDR_WIDTH:])
    s_axi_arlen = Signal(intbv(0)[8:])
    s_axi_arsize = Signal(intbv(0)[3:])
    s_axi_arburst = Signal(intbv(0)[2:])
    s_axi_arlock = Signal(bool(0))
    s_axi_arcache = Signal(intbv(0)[4:])
    s_axi_arprot = Signal(intbv(0)[3:])
    s_axi_arqos = Signal(intbv(0)[4:])
    s_axi_arregion = Signal(intbv(0)[4:])
    s_axi_aruser = Signal(intbv(0)[ARUSER_WIDTH:])
    s_axi_arvalid = Signal(bool(0))
    s_axi_rready = Signal(bool(0))
    m_axi_awready = Signal(bool(0))
    m_axi_wready = Signal(bool(0))
    m_axi_bid = Signal(intbv(0)[ID_WIDTH:])
    m_axi_bresp = Signal(intbv(0)[2:])
    m_axi_buser = Signal(intbv(0)[BUSER_WIDTH:])
    m_axi_bvalid = Signal(bool(0))
    m_axi_arready = Signal(bool(0))
    m_axi_rid = Signal(intbv(0)[ID_WIDTH:])
    m_axi_rdata = Signal(intbv(0)[M_DATA_WIDTH:])
    m_axi_rresp = Signal(intbv(0)[2:])
    m_axi_rlast = Signal(bool(0))
    m_axi_ruser = Signal(intbv(0)[RUSER_WIDTH:])
    m_axi_rvalid = Signal(bool(0))

    # Outputs
    s_axi_awready = Signal(bool(0))
    s_axi_wready = Signal(bool(0))
    s_axi_bid = Signal(intbv(0)[ID_WIDTH:])
    s_axi_bresp = Signal(intbv(0)[2:])
    s_axi_buser = Signal(intbv(0)[BUSER_WIDTH:])
    s_axi_bvalid = Signal(bool(0))
    s_axi_arready = Signal(bool(0))
    s_axi_rid = Signal(intbv(0)[ID_WIDTH:])
    s_axi_rdata = Signal(intbv(0)[S_DATA_WIDTH:])
    s_axi_rresp = Signal(intbv(0)[2:])
    s_axi_rlast = Signal(bool(0))
    s_axi_ruser = Signal(intbv(0)[RUSER_WIDTH:])
    s_axi_rvalid = Signal(bool(0))
    m_axi_awid = Signal(intbv(0)[ID_WIDTH:])
    m_axi_awaddr = Signal(intbv(0)[ADDR_WIDTH:])
    m_axi_awlen = Signal(intbv(0)[8:])
    m_axi_awsize = Signal(intbv(0)[3:])
    m_axi_awburst = Signal(intbv(0)[2:])
    m_axi_awlock = Signal(bool(0))
    m_axi_awcache = Signal(intbv(0)[4:])
    m_axi_awprot = Signal(intbv(0)[3:])
    m_axi_awqos = Signal(intbv(0)[4:])
    m_axi_awregion = Signal(intbv(0)[4:])
    m_axi_awuser = Signal(intbv(0)[AWUSER_WIDTH:])
    m_axi_awvalid = Signal(bool(0))
    m_axi_wdata = Signal(intbv(0)[M_DATA_WIDTH:])
    m_axi_wstrb = Signal(intbv(0)[M_STRB_WIDTH:])
    m_axi_wlast = Signal(bool(0))
    m_axi_wuser = Signal(intbv(0)[WUSER_WIDTH:])
    m_axi_wvalid = Signal(bool(0))
    m_axi_bready = Signal(bool(0))
    m_axi_arid = Signal(intbv(0)[ID_WIDTH:])
    m_axi_araddr = Signal(intbv(0)[ADDR_WIDTH:])
    m_axi_arlen = Signal(intbv(0)[8:])
    m_axi_arsize = Signal(intbv(0)[3:])
    m_axi_arburst = Signal(intbv(0)[2:])
    m_axi_arlock = Signal(bool(0))
    m_axi_arcache = Signal(intbv(0)[4:])
    m_axi_arprot = Signal(intbv(0)[3:])
    m_axi_arqos = Signal(intbv(0)[4:])
    m_axi_arregion = Signal(intbv(0)[4:])
    m_axi_aruser = Signal(intbv(0)[ARUSER_WIDTH:])
    m_axi_arvalid = Signal(bool(0))
    m_axi_rready = Signal(bool(0))

    # AXI4 master
    axi_master_inst = axi.AXIMaster()
    axi_master_pause = Signal(bool(False))

    axi_master_logic = axi_master_inst.create_logic(
        clk,
        rst,
        m_axi_awid=s_axi_awid,
        m_axi_awaddr=s_axi_awaddr,
        m_axi_awlen=s_axi_awlen,
        m_axi_awsize=s_axi_awsize,
        m_axi_awburst=s_axi_awburst,
        m_axi_awlock=s_axi_awlock,
        m_axi_awcache=s_axi_awcache,
        m_axi_awprot=s_axi_awprot,
        m_axi_awqos=s_axi_awqos,
        m_axi_awregion=s_axi_awregion,
        m_axi_awvalid=s_axi_awvalid,
        m_axi_awready=s_axi_awready,
        m_axi_wdata=s_axi_wdata,
        m_axi_wstrb=s_axi_wstrb,
        m_axi_wlast=s_axi_wlast,
        m_axi_wvalid=s_axi_wvalid,
        m_axi_wready=s_axi_wready,
        m_axi_bid=s_axi_bid,
        m_axi_bresp=s_axi_bresp,
        m_axi_bvalid=s_axi_bvalid,
        m_axi_bready=s_axi_bready,
        m_axi_arid=s_axi_arid,
        m_axi_araddr=s_axi_araddr,
        m_axi_arlen=s_axi_arlen,
        m_axi_arsize=s_axi_arsize,
        m_axi_arburst=s_axi_arburst,
        m_axi_arlock=s_axi_arlock,
        m_axi_arcache=s_axi_arcache,
        m_axi_arprot=s_axi_arprot,
        m_axi_arqos=s_axi_arqos,
        m_axi_arregion=s_axi_arregion,
        m_axi_arvalid=s_axi_arvalid,
        m_axi_arready=s_axi_arready,
        m_axi_rid=s_axi_rid,
        m_axi_rdata=s_axi_rdata,
        m_axi_rresp=s_axi_rresp,
        m_axi_rlast=s_axi_rlast,
        m_axi_rvalid=s_axi_rvalid,
        m_axi_rready=s_axi_rready,
        pause=axi_master_pause,
        name='master'
    )

    # AXI4 RAM model
    axi_ram_inst = axi.AXIRam(2**16)
    axi_ram_pause = Signal(bool(False))

    axi_ram_port0 = axi_ram_inst.create_port(
        clk,
        s_axi_awid=m_axi_awid,
        s_axi_awaddr=m_axi_awaddr,
        s_axi_awlen=m_axi_awlen,
        s_axi_awsize=m_axi_awsize,
        s_axi_awburst=m_axi_awburst,
        s_axi_awlock=m_axi_awlock,
        s_axi_awcache=m_axi_awcache,
        s_axi_awprot=m_axi_awprot,
        s_axi_awvalid=m_axi_awvalid,
        s_axi_awready=m_axi_awready,
        s_axi_wdata=m_axi_wdata,
        s_axi_wstrb=m_axi_wstrb,
        s_axi_wlast=m_axi_wlast,
        s_axi_wvalid=m_axi_wvalid,
        s_axi_wready=m_axi_wready,
        s_axi_bid=m_axi_bid,
        s_axi_bresp=m_axi_bresp,
        s_axi_bvalid=m_axi_bvalid,
        s_axi_bready=m_axi_bready,
        s_axi_arid=m_axi_arid,
        s_axi_araddr=m_axi_araddr,
        s_axi_arlen=m_axi_arlen,
        s_axi_arsize=m_axi_arsize,
        s_axi_arburst=m_axi_arburst,
        s_axi_arlock=m_axi_arlock,
        s_axi_arcache=m_axi_arcache,
        s_axi_arprot=m_axi_arprot,
        s_axi_arvalid=m_axi_arvalid,
        s_axi_arready=m_axi_arready,
        s_axi_rid=m_axi_rid,
        s_axi_rdata=m_axi_rdata,
        s_axi_rresp=m_axi_rresp,
        s_axi_rlast=m_axi_rlast,
        s_axi_rvalid=m_axi_rvalid,
        s_axi_rready=m_axi_rready,
        pause=axi_ram_pause,
        name='port0'
    )

    # DUT
    if os.system(build_cmd):
        raise Exception("Error running build command")

    dut = Cosimulation(
        "vvp -m myhdl %s.vvp -lxt2" % testbench,
        clk=clk,
        rst=rst,
        current_test=current_test,
        s_axi_awid=s_axi_awid,
        s_axi_awaddr=s_axi_awaddr,
        s_axi_awlen=s_axi_awlen,
        s_axi_awsize=s_axi_awsize,
        s_axi_awburst=s_axi_awburst,
        s_axi_awlock=s_axi_awlock,
        s_axi_awcache=s_axi_awcache,
        s_axi_awprot=s_axi_awprot,
        s_axi_awqos=s_axi_awqos,
        s_axi_awregion=s_axi_awregion,
        s_axi_awuser=s_axi_awuser,
        s_axi_awvalid=s_axi_awvalid,
        s_axi_awready=s_axi_awready,
        s_axi_wdata=s_axi_wdata,
        s_axi_wstrb=s_axi_wstrb,
        s_axi_wlast=s_axi_wlast,
        s_axi_wuser=s_axi_wuser,
        s_axi_wvalid=s_axi_wvalid,
        s_axi_wready=s_axi_wready,
        s_axi_bid=s_axi_bid,
        s_axi_bresp=s_axi_bresp,
        s_axi_buser=s_axi_buser,
        s_axi_bvalid=s_axi_bvalid,
        s_axi_bready=s_axi_bready,
        s_axi_arid=s_axi_arid,
        s_axi_araddr=s_axi_araddr,
        s_axi_arlen=s_axi_arlen,
        s_axi_arsize=s_axi_arsize,
        s_axi_arburst=s_axi_arburst,
        s_axi_arlock=s_axi_arlock,
        s_axi_arcache=s_axi_arcache,
        s_axi_arprot=s_axi_arprot,
        s_axi_arqos=s_axi_arqos,
        s_axi_arregion=s_axi_arregion,
        s_axi_aruser=s_axi_aruser,
        s_axi_arvalid=s_axi_arvalid,
        s_axi_arready=s_axi_arready,
        s_axi_rid=s_axi_rid,
        s_axi_rdata=s_axi_rdata,
        s_axi_rresp=s_axi_rresp,
        s_axi_rlast=s_axi_rlast,
        s_axi_ruser=s_axi_ruser,
        s_axi_rvalid=s_axi_rvalid,
        s_axi_rready=s_axi_rready,
        m_axi_awid=m_axi_awid,
        m_axi_awaddr=m_axi_awaddr,
        m_axi_awlen=m_axi_awlen,
        m_axi_awsize=m_axi_awsize,
        m_axi_awburst=m_axi_awburst,
        m_axi_awlock=m_axi_awlock,
        m_axi_awcache=m_axi_awcache,
        m_axi_awprot=m_axi_awprot,
        m_axi_awqos=m_axi_awqos,
        m_axi_awregion=m_axi_awregion,
        m_axi_awuser=m_axi_awuser,
        m_axi_awvalid=m_axi_awvalid,
        m_axi_awready=m_axi_awready,
        m_axi_wdata=m_axi_wdata,
        m_axi_wstrb=m_axi_wstrb,
        m_axi_wlast=m_axi_wlast,
        m_axi_wuser=m_axi_wuser,
        m_axi_wvalid=m_axi_wvalid,
        m_axi_wready=m_axi_wready,
        m_axi_bid=m_axi_bid,
        m_axi_bresp=m_axi_bresp,
        m_axi_buser=m_axi_buser,
        m_axi_bvalid=m_axi_bvalid,
        m_axi_bready=m_axi_bready,
        m_axi_arid=m_axi_arid,
        m_axi_araddr=m_axi_araddr,
        m_axi_arlen=m_axi_arlen,
        m_axi_arsize=m_axi_arsize,
        m_axi_arburst=m_axi_arburst,
        m_axi_arlock=m_axi_arlock,
        m_axi_arcache=m_axi_arcache,
        m_axi_arprot=m_axi_arprot,
        m_axi_arqos=m_axi_arqos,
        m_axi_arregion=m_axi_arregion,
        m_axi_aruser=m_axi_aruser,
        m_axi_arvalid=m_axi_arvalid,
        m_axi_arready=m_axi_arready,
        m_axi_rid=m_axi_rid,
        m_axi_rdata=m_axi_rdata,
        m_axi_rresp=m_axi_rresp,
        m_axi_rlast=m_axi_rlast,
        m_axi_ruser=m_axi_ruser,
        m_axi_rvalid=m_axi_rvalid,
        m_axi_rready=m_axi_rready
    )

    @always(delay(4))
    def clkgen():
        clk.next = not clk

    def wait_normal():
        while not axi_master_inst.idle():
            yield clk.posedge

    def wait_pause_master():
        while not axi_master_inst.idle():
            axi_master_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            axi_master_pause.next = False
            yield clk.posedge

    def wait_pause_slave():
        while not axi_master_inst.idle():
            axi_ram_pause.next = True
            yield clk.posedge
            yield clk.posedge
            yield clk.posedge
            axi_ram_pause.next = False
            yield clk.posedge

    @instance
    def check():
        yield delay(100)
        yield clk.posedge
        rst.next = 1
        yield clk.posedge
        rst.next = 0
        yield clk.posedge
        yield delay(100)
        yield clk.posedge

        # testbench stimulus

        yield clk.posedge
        print("test 1: write")
        current_test.next = 1

        addr = 4
        test_data = b'\x11\x22\x33\x44'

        axi_master_inst.init_write(addr, test_data)

        yield axi_master_inst.wait()
        yield clk.posedge

        data = axi_ram_inst.read_mem(addr&0xffffff80, 32)
        for i in range(0, len(data), 16):
            print(" ".join(("{:02x}".format(c) for c in bytearray(data[i:i+16]))))

        assert axi_ram_inst.read_mem(addr, len(test_data)) == test_data

        yield delay(100)

        yield clk.posedge
        print("test 2: read")
        current_test.next = 2

        addr = 4
        test_data = b'\x11\x22\x33\x44'

        axi_ram_inst.write_mem(addr, test_data)

        axi_master_inst.init_read(addr, len(test_data))

        yield axi_master_inst.wait()
        yield clk.posedge

        data = axi_master_inst.get_read_data()
        assert data[0] == addr
        assert data[1] == test_data

        yield delay(100)

        yield clk.posedge
        print("test 3: various writes")
        current_test.next = 3

        for length in list(range(1,8))+[1024]:
            for offset in list(range(4,8))+[4096-4]:
                for size, cache in ((2, 0b0011), (2, 0b0000), (1, 0b0011), (0, 0b0011)):
                    for wait in wait_normal, wait_pause_master, wait_pause_slave:
                        print("length %d, offset %d, size %d, cache %d"% (length, offset, size, cache))
                        #addr = 256*(16*offset+length)+offset
                        addr = offset
                        test_data = bytearray([x%256 for x in range(length)])

                        axi_ram_inst.write_mem(addr&0xffffff80, b'\xAA'*(length+256))
                        axi_master_inst.init_write(addr, test_data, size=size, cache=cache)

                        yield wait()
                        yield clk.posedge

                        data = axi_ram_inst.read_mem(addr&0xffffff80, 32)
                        for i in range(0, len(data), 16):
                            print(" ".join(("{:02x}".format(c) for c in bytearray(data[i:i+16]))))

                        assert axi_ram_inst.read_mem(addr, length) == test_data
                        assert axi_ram_inst.read_mem(addr-1, 1) == b'\xAA'
                        assert axi_ram_inst.read_mem(addr+length, 1) == b'\xAA'

        yield delay(100)

        yield clk.posedge
        print("test 4: various reads")
        current_test.next = 4

        for length in list(range(1,8))+[1024]:
            for offset in list(range(4,8))+[4096-4]:
                for size, cache in ((2, 0b0011), (2, 0b0000), (1, 0b0011), (0, 0b0011)):
                    for wait in wait_normal, wait_pause_master, wait_pause_slave:
                        print("length %d, offset %d, size %d, cache %d"% (length, offset, size, cache))
                        #addr = 256*(16*offset+length)+offset
                        addr = offset
                        test_data = bytearray([x%256 for x in range(length)])

                        axi_ram_inst.write_mem(addr, test_data)

                        axi_master_inst.init_read(addr, length, size=size, cache=cache)

                        yield wait()
                        yield clk.posedge

                        data = axi_master_inst.get_read_data()
                        assert data[0] == addr
                        assert data[1] == test_data

        yield delay(100)

        raise StopSimulation

    return instances()

def test_bench():
    sim = Simulation(bench())
    sim.run()

if __name__ == '__main__':
    print("Running test...")
    test_bench()
