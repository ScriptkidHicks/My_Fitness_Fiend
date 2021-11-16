import jwtDecode from "jwt-decode";
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

// this is the first time quiz page. It will be gated by both login status, and whether they have completed the first time quiz. If they have then we will send them back to the monster main page. There will also be no ribbon bar on this page, to prevent them from manually
function FirstTimeQuizPage() {
  const theme = useContext(ColorContext);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  let usertoken = jwtDecode(localStorage.getItem("id_token"));
  let user_id = usertoken.user_id;

  useEffect(() => {
    if (usertoken === null || usertoken === undefined) {
      navigate("/SignIn");
    } else {
      if (usertoken.exp * 1000 < Date.now()) {
        navigate("/SignIn");
      } else {
        const quizGate = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            user_token: user_id,
          },
        };

        fetch("/get_user_info", quizGate)
          .then((response) => {
            if (response.status !== 201) {
              return null;
            } else {
              return response.json();
            }
          })
          .then((json) => {
            if (json.has_finished_quiz) {
              navigate("/MonsterPage");
            } else {
              setLoading(false);
            }
          });
      }
    }
  });

  if (loading) {
    return (
      <LoadingWrapper theme={theme}>
        <LoadingText theme={theme}>
          <LoadingTextWrapper theme={theme}>Loading...</LoadingTextWrapper>
        </LoadingText>
      </LoadingWrapper>
    );
  } else {
    return <Body>Welcome to the first time quiz</Body>;
  }
}

export default FirstTimeQuizPage;

const Body = styled.div``;

const LoadingWrapper = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
`;

const LoadingTextWrapper = styled.div`
  background-color: ${(props) => props.theme.secondaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  width: max(20vw, 200px);
  height: 10vh;
  border-radius: 20px;
  box-shadow: -4px 4px 14px black;
`;

const LoadingText = styled.h1`
  color: ${(props) => props.theme.primaryText};
  font-weight: bolder;
  text-align: center;
`;
