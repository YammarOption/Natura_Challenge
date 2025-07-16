local lvAddr = 0xd18C
local battleAddr = 0xd057
local currAttStat = 0xd025
local monExpStart = 0xd179
local HpExpStart = 0xd17c

local PPaddrsStart=0xd188
local currPrec = 0xcfd6
local currmove = 0xcfd2
local frame_pause = 60*8
local framecounter = 0
local sock = nil

function ST_stop()
	if not sock then return end
	console:log("sock Test: Shutting down")
	sock:close()
	sock = nil
end

function opensock()
	console:log("--------------------------------")
    ST_stop()
	console:log("sock Test: Connecting to 127.0.0.1:9999")
	if sock then return end
	sock = socket.tcp()
	if sock:connect("127.0.0.1", 9999) then
		console:log("sock Test: Connected")
	else
		console:log("sock Test: Failed to connect")
		ST_stop()
	end
end

function updateTracker()
	--console:log("Sending data")
    local lv = emu:read8(lvAddr)
    local hp = emu:read8(lvAddr+1)<<8|emu:read8(lvAddr+2)
    local att = emu:read8(lvAddr+3)<<8|emu:read8(lvAddr+4)
    local df = emu:read8(lvAddr+5)<<8|emu:read8(lvAddr+6)
    local spd = emu:read8(lvAddr+7)<<8|emu:read8(lvAddr+8)
    local spe = emu:read8(lvAddr+9)<<8|emu:read8(lvAddr+10)
	
	local isinbattle=emu:read8(battleAddr)
	local battleatt = emu:read8(currAttStat+1)|emu:read8(currAttStat)<<8
    local battledf = emu:read8(currAttStat+3)|emu:read8(currAttStat+2)<<8
    local battlespd = emu:read8(currAttStat+5)|emu:read8(currAttStat+4)<<8
    local battlespe = emu:read8(currAttStat+7)|emu:read8(currAttStat+6)<<8

	local expstats=emu:read8(monExpStart+2)|emu:read8(monExpStart+1)<<8|emu:read8(monExpStart)<<16
	local HPstatExp=emu:read8(HpExpStart+1) | emu:read8(HpExpStart) << 8
	local Attexpstats = emu:read8(HpExpStart+3) | emu:read8(HpExpStart+2) << 8
	local Defexpstats = emu:read8(HpExpStart+5) | emu:read8(HpExpStart+4)<< 8 
	local Spdexpstats = emu:read8(HpExpStart+7) | emu:read8(HpExpStart+6)<< 8 
	local Specxpstats = emu:read8(HpExpStart+9) | emu:read8(HpExpStart+8)<< 8 

	local movePP1 = emu:read8(PPaddrsStart)
	local movePP2 = emu:read8(PPaddrsStart+1)
	local movePP3 = emu:read8(PPaddrsStart+2)
	local movePP4 = emu:read8(PPaddrsStart+3)
	local prec = emu:read8(currPrec)
	local move = emu:read8(currmove)

    if not sock then return end
	sock:send(""..string.format("%x",lv)..
			"@"..string.format("%x",hp)..
			"@"..string.format("%x",spd)..
			"@"..string.format("%x",att)..
			"@"..string.format("%x",spe)..
			"@"..string.format("%x",df)..
			"@"..string.format("%x",isinbattle)..
			"@"..string.format("%x",battlespd)..
			"@"..string.format("%x", battleatt)..
			"@"..string.format("%x",battlespe)..
			"@"..string.format("%x",battledf)..
			"@"..string.format("%x",expstats)..
			"@"..string.format("%x",HPstatExp)..
			"@"..string.format("%x",Spdexpstats)..
			"@"..string.format("%x",Attexpstats)..
			"@"..string.format("%x",Specxpstats)..
			"@"..string.format("%x",Defexpstats)..
			"@"..string.format("%x",movePP1)..
			"@"..string.format("%x",movePP2)..
			"@"..string.format("%x",movePP3)..
			"@"..string.format("%x",movePP4)..
			"@"..string.format("%x",move)..
			"@"..string.format("%x",prec)
		)
end


function updateBuffer()
    framecounter=framecounter+1
    if framecounter >= frame_pause then
    	updateTracker()
        framecounter=0
    end
end

callbacks:add("frame", updateBuffer)
callbacks:add("start",opensock)
callbacks:add("error",ST_stop)
callbacks:add("stop",ST_stop)
callbacks:add("shutdown",ST_stop)
