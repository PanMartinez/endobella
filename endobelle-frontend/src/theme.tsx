'use client'
import { createTheme } from '@mui/material/styles';
import { Mulish } from 'next/font/google'

const font = Mulish({
  weight: ['300'],
  subsets: ['latin'],
  display: 'swap',
})

const theme = createTheme(
  {
    colorSchemes: { light: true, dark: true },
    palette: {
      primary: {
        main: '#000000',
      },
      secondary: {
        main: '#ffffff',
      },
    },
    typography: {
      fontFamily: font.style.fontFamily,
    },
  },
)

export default theme