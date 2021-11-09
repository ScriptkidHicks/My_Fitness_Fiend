import { useContext } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

function MonsterPage() {
  const theme = useContext(ColorContext);
  return <Body theme={theme}>Monster Page</Body>;
}

export default MonsterPage;

const Body = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
`;
