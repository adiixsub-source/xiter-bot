--============================================--
-- Adiiiiiiix script
-- قائمة أدوات اختبار الثغرات
-- الأداة 1: COIN MAGNET v2 (نفس الوظيفة بدون تغيير)
--============================================--

local player = game.Players.LocalPlayer
local coins = player:WaitForChild("leaderstats"):WaitForChild("Coins")

--===== حالة الأداة (كما هي بالضبط) =====--
local magnetOn = false
local busy = false
local stolenTotal = 0

--===== الواجهة الرئيسية =====--
local gui = Instance.new("ScreenGui")
gui.Name = "AdiiiiiiixScript"
gui.ResetOnSpawn = false
gui.Parent = player:WaitForChild("PlayerGui")

-- زر فتح/إغلاق القائمة (صغير دائري)
local openBtn = Instance.new("TextButton")
openBtn.Size = UDim2.new(0, 46, 0, 46)
openBtn.Position = UDim2.new(0, 12, 0.5, -23)
openBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 45)
openBtn.TextColor3 = Color3.fromRGB(255, 200, 0)
openBtn.Font = Enum.Font.GothamBold
openBtn.TextSize = 20
openBtn.Text = "☰"
openBtn.Active = true
openBtn.Draggable = true
openBtn.Parent = gui
Instance.new("UICorner", openBtn).CornerRadius = UDim.new(1, 0)
local openStroke = Instance.new("UIStroke", openBtn)
openStroke.Color = Color3.fromRGB(255, 200, 0)
openStroke.Thickness = 1.5

-- اللوحة الرئيسية
local panel = Instance.new("Frame")
panel.Size = UDim2.new(0, 250, 0, 320)
panel.Position = UDim2.new(0, 70, 0.5, -160)
panel.BackgroundColor3 = Color3.fromRGB(22, 22, 32)
panel.BorderSizePixel = 0
panel.Visible = false
panel.Active = true
panel.Draggable = true
panel.Parent = gui
Instance.new("UICorner", panel).CornerRadius = UDim.new(0, 14)
local panelStroke = Instance.new("UIStroke", panel)
panelStroke.Color = Color3.fromRGB(255, 200, 0)
panelStroke.Thickness = 1.5
panelStroke.Transparency = 0.4

-- العنوان
local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, -20, 0, 40)
title.Position = UDim2.new(0, 10, 0, 8)
title.BackgroundTransparency = 1
title.TextColor3 = Color3.fromRGB(255, 200, 0)
title.Font = Enum.Font.GothamBold
title.TextSize = 17
title.Text = "Adiiiiiiix script"
title.Parent = panel

local titleLine = Instance.new("Frame")
titleLine.Size = UDim2.new(1, -20, 0, 2)
titleLine.Position = UDim2.new(0, 10, 0, 46)
titleLine.BackgroundColor3 = Color3.fromRGB(255, 200, 0)
titleLine.BackgroundTransparency = 0.5
titleLine.BorderSizePixel = 0
titleLine.Parent = panel

-- قائمة الأدوات (قابلة للتمرير)
local list = Instance.new("ScrollingFrame")
list.Size = UDim2.new(1, -16, 1, -110)
list.Position = UDim2.new(0, 8, 0, 56)
list.BackgroundTransparency = 1
list.ScrollBarThickness = 4
list.ScrollBarImageColor3 = Color3.fromRGB(255, 200, 0)
list.CanvasSize = UDim2.new(0, 0, 0, 0)
list.AutomaticCanvasSize = Enum.AutomaticSize.Y
list.Parent = panel

local layout = Instance.new("UIListLayout", list)
layout.Padding = UDim.new(0, 8)
layout.SortOrder = Enum.SortOrder.LayoutOrder

-- شريط الحالة أسفل اللوحة
local statusBar = Instance.new("TextLabel")
statusBar.Size = UDim2.new(1, -20, 0, 40)
statusBar.Position = UDim2.new(0, 10, 1, -48)
statusBar.BackgroundColor3 = Color3.fromRGB(15, 15, 22)
statusBar.TextColor3 = Color3.fromRGB(180, 180, 180)
statusBar.Font = Enum.Font.Gotham
statusBar.TextSize = 12
statusBar.Text = "Stolen: 0 DH"
statusBar.Parent = panel
Instance.new("UICorner", statusBar).CornerRadius = UDim.new(0, 8)

-- فتح/إغلاق اللوحة
openBtn.MouseButton1Click:Connect(function()
    panel.Visible = not panel.Visible
end)

--============================================--
-- دالة إنشاء بطاقة أداة في القائمة
--============================================--
local function makeToolCard(toolName, description)
    local card = Instance.new("Frame")
    card.Size = UDim2.new(1, -4, 0, 72)
    card.BackgroundColor3 = Color3.fromRGB(32, 32, 46)
    card.BorderSizePixel = 0
    card.Parent = list
    Instance.new("UICorner", card).CornerRadius = UDim.new(0, 10)

    local nameLbl = Instance.new("TextLabel")
    nameLbl.Size = UDim2.new(1, -70, 0, 24)
    nameLbl.Position = UDim2.new(0, 12, 0, 8)
    nameLbl.BackgroundTransparency = 1
    nameLbl.TextColor3 = Color3.new(1, 1, 1)
    nameLbl.Font = Enum.Font.GothamBold
    nameLbl.TextSize = 14
    nameLbl.TextXAlignment = Enum.TextXAlignment.Left
    nameLbl.Text = toolName
    nameLbl.Parent = card

    local descLbl = Instance.new("TextLabel")
    descLbl.Size = UDim2.new(1, -70, 0, 34)
    descLbl.Position = UDim2.new(0, 12, 0, 30)
    descLbl.BackgroundTransparency = 1
    descLbl.TextColor3 = Color3.fromRGB(150, 150, 160)
    descLbl.Font = Enum.Font.Gotham
    descLbl.TextSize = 11
    descLbl.TextWrapped = true
    descLbl.TextXAlignment = Enum.TextXAlignment.Left
    descLbl.TextYAlignment = Enum.TextYAlignment.Top
    descLbl.Text = description
    descLbl.Parent = card

    local toggle = Instance.new("TextButton")
    toggle.Size = UDim2.new(0, 52, 0, 26)
    toggle.Position = UDim2.new(1, -62, 0, 23)
    toggle.BackgroundColor3 = Color3.fromRGB(120, 120, 120)
    toggle.TextColor3 = Color3.new(1, 1, 1)
    toggle.Font = Enum.Font.GothamBold
    toggle.TextSize = 12
    toggle.Text = "OFF"
    toggle.Parent = card
    Instance.new("UICorner", toggle).CornerRadius = UDim.new(1, 0)

    return toggle
end

--===== بطاقة COIN MAGNET =====--
local magnetToggle = makeToolCard(
    "COIN MAGNET v2",
    "Teleport snatch: grabs dropped cash and returns to your spot"
)

magnetToggle.MouseButton1Click:Connect(function()
    magnetOn = not magnetOn
    magnetToggle.Text = magnetOn and "ON" or "OFF"
    magnetToggle.BackgroundColor3 = magnetOn and Color3.fromRGB(0, 170, 90)
        or Color3.fromRGB(120, 120, 120)
end)

--============================================--
-- محرك النقل والسرقة (بدون أي تغيير)
--============================================--
local function snatch(cashObj)
    if busy or not magnetOn then return end
    local char = player.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local part = cashObj:IsA("BasePart") and cashObj
        or cashObj:FindFirstChildWhichIsA("BasePart", true)
    if not part then return end

    busy = true
    local returnPos = hrp.CFrame
    local before = coins.Value

    -- 1) انتقال خاطف فوق الكاش
    hrp.CFrame = part.CFrame + Vector3.new(0, 3, 0)
    task.wait(0.15)

    -- 2) ضغط الـ prompt + اللمس يعمل تلقائياً (نحن فوقه)
    local prompt = cashObj:FindFirstChildOfClass("ProximityPrompt", true)
    if prompt then
        pcall(function() fireproximityprompt(prompt) end)
    end
    task.wait(0.25)

    -- 3) العودة كأن شيئاً لم يحدث
    if hrp.Parent then
        hrp.CFrame = returnPos
    end

    if coins.Value > before then
        local amount = coins.Value - before
        stolenTotal += amount
        statusBar.Text = "Stolen: " .. stolenTotal .. " DH"
        warn("[Adiiiiiiix] Snatched +" .. amount .. " DH!")
    end
    busy = false
end

-- صيد فوري لأي كاش جديد
workspace.ChildAdded:Connect(function(obj)
    if obj.Name:lower():find("cash") then
        task.wait(0.05)
        pcall(snatch, obj)
    end
end)

-- مسح دوري للكاش الموجود
task.spawn(function()
    while gui.Parent do
        if magnetOn and not busy then
            for _, obj in ipairs(workspace:GetChildren()) do
                if obj.Name:lower():find("cash") then
                    pcall(snatch, obj)
                end
            end
        end
        task.wait(0.4)
    end
end)

print("[Adiiiiiiix script] Ready! Press the round button to open")
