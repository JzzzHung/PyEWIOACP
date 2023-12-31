typedef struct CommandPinOperate
{
    String name;
    const char *cmd;
    int size;
} CMD_PO;

typedef struct CommandFreeStyle
{
    String name;
    void (*fnc)();
} CMD_FS;

CMD_FS commandfsList[] = {
    {"=", &Switch_ServoMagnetic},
    // {"1", &FirstReagentInject},
    // {"2", &SecondReagentInject},
    // {"3", &ThirdReagentInject},
};

CMD_PO commandpoList[] = {
    {"b", b, arrayLength(b)},
    {"QFPXMix", QFPXMix, arrayLength(QFPXMix)},
    {"QFPMix", QFPMix, arrayLength(QFPMix)},
    {"DFPMix", DFPMix, arrayLength(DFPMix)},
    {"LeftIN", LeftIN, arrayLength(LeftIN)},
    {"RightIN", RightIN, arrayLength(RightIN)},
    {"ToLeftOut", ToLeftOut, arrayLength(ToLeftOut)},
    {"ToRightOut", ToRightOut, arrayLength(ToRightOut)},
    {"LeftRightIN", LeftRightIN, arrayLength(LeftRightIN)},
    {"Mix", Mix, arrayLength(Mix)},
    {"ToTopOut", ToTopOut, arrayLength(ToTopOut)},
    {"ToBottomOut", ToBottomOut, arrayLength(ToBottomOut)},
    {"TopIN", TopIN, arrayLength(TopIN)},
    {"BottomIN", BottomIN, arrayLength(BottomIN)},
    {"LRinAndMix", LRinAndMix, arrayLength(LRinAndMix)},
};

byte channel_selector(String str)
{
    // Default
    if (str == "@") {
        pin_operate(Pause, arrayLength(Pause));
        return 0;
    }

    // for pin operate
    for (int i = 0; i < arrayLength(commandpoList); i++)
    {
        if (str == commandpoList[i].name)
        {
            pin_operate(commandpoList[i].cmd, commandpoList[i].size);
            return 0;
        }
    }

    // for not pin operate
    for (int i = 0; i < arrayLength(commandfsList); i++)
    {
        if (str == commandfsList[i].name)
        {
            commandfsList[i].fnc();
            return 0;
        }
    }

    return 1;
}
