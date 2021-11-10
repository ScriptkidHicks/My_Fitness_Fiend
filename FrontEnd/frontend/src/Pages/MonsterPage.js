import { useContext } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

function parseJWT(token) {
  try {
    return JSON.parse(atob(token.split(",")[1]));
  } catch (e) {
    return null;
  }
}

function MonsterPage() {
  const navigate = useNavigate();
  let token = localStorage.getItem("id_token");
  console.log("token", token);
  token = parseJWT(token);
  console.log("parsed:", token);
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
