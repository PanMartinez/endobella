"use client"

import AppBar from "@mui/material/AppBar"
import Grid from "@mui/material/Grid"
import Toolbar from "@mui/material/Toolbar"
import Typography from "@mui/material/Typography"

import MenuCategories from "@/components/MenuCategories"
import ModeSwitch from "@/components/ui/ModeSwitch"

export default function Header() {
  return (
    <AppBar
      component="header"
      sx={{
        backgroundColor: 'background.paper',
        position: 'sticky',
        top: 0,
        zIndex: (theme) => theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar>
        <Grid container sx={{ flexGrow: 1 }}>
          <Grid
            size={9}
            display={'flex'}
            justifyContent={'flex-start'}
            alignItems={'center'}
          >
            <Typography color="primary" variant="h6">
              Endobelle Logo
            </Typography>
          </Grid>

          <Grid size={2}
                display={'flex'}
                justifyContent={'flex-end'}
                alignItems={'center'}
          >
            <MenuCategories/>
          </Grid>

          <Grid size={1}
                display={'flex'}
                justifyContent={'flex-end'}
                alignItems={'center'}

          >
            <ModeSwitch/>
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  )
}