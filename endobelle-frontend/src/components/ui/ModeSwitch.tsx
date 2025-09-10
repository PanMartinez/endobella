"use client";

import * as React from "react";
import LightMode from "@mui/icons-material/LightMode";
import ModeNight from "@mui/icons-material/ModeNight";
import AutoMode from "@mui/icons-material/AutoMode";
import IconButton from "@mui/material/IconButton";
import { useColorScheme } from "@mui/material/styles";


const modes: Array<"system" | "light" | "dark"> = ["system", "light", "dark"]

export default function ModeSwitch() {
  const { mode, setMode } = useColorScheme()

  if (!mode) {
    return null
  }

  const handleModeChange = () => {
    const currentMode = modes.indexOf(mode)
    const nextMode = (currentMode + 1) % modes.length
    setMode(modes[nextMode])
  }

    const renderIcon = () => {
    switch (mode) {
      case 'light':
        return <LightMode fontSize='small'/>;
      case 'dark':
        return <ModeNight fontSize='small'/>;
      default:
        return <AutoMode fontSize='small'/>;
    }
  };

  return (
    <IconButton
    onClick={handleModeChange}>
      {renderIcon()}
    </IconButton>
  )

}