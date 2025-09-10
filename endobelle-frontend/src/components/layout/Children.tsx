import * as React from "react";
import Container from "@mui/material/Container";


export default function Children({children}: { children: React.ReactNode}) {
  return (
    <Container sx={{ flex: 1}}>
      {children}
    </Container>
  )
}