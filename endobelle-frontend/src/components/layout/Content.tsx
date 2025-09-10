import * as React from 'react';
import Box from "@mui/material/Box";


export default function Content({ children } : { children: React.ReactNode })  {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      { children }
    </Box>
  )
}