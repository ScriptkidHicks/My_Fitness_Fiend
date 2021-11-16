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

  const [species, setSepecies] = useState(null);
  const [experience, setExperience] = useState(null);
  const [daysPerWeek, setDaysPerWeek] = useState(null);
  const [availableEquipment, setAvailableEquipment] = useState(null);

  const [introductionVisibility, setIntroductionVisibility] = useState(true);
  const [speciesModalVisibility, setSpeciesModalVisibility] = useState(false);
  const [experienceModalVisibility, setExperienceModalVisibility] =
    useState(false);
  const [daysPerWeekModalVisibility, setDaysPerWeekModalVisibility] =
    useState(false);
  const [
    availableEquipmentModalVisibility,
    setAvailableEquipmentModalVisiblity,
  ] = useState(false);

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
    return (
      <Body theme={theme}>
        {introductionVisibility ? (
          <QuizSection theme={theme}>
            <IntroductionText>
              Welcome to the first time quiz! We'll gather some information
              about what your workout life looks like, and what monster is right
              for you!
            </IntroductionText>
            <NextButton
              theme={theme}
              onClick={() => {
                setIntroductionVisibility(false);
                setSpeciesModalVisibility(true);
              }}
            >
              Take Quiz
            </NextButton>
          </QuizSection>
        ) : null}
        {speciesModalVisibility ? (
          <QuizSection theme={theme}>
            <NextButton>Next</NextButton>
          </QuizSection>
        ) : null}
      </Body>
    );
  }
}

export default FirstTimeQuizPage;

const Body = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
`;

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

const QuizSection = styled.div`
  border: 2px solid black;
  margin-bottom: 20vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 60vh;
  width: min(80vw, 600px);
  background-color: ${(props) => props.theme.secondaryBackground};
  box-shadow: -8px 8px 20px ${(props) => props.theme.secondaryBackgroundShadow};
  border-radius: 20px;
`;

const IntroductionText = styled.h3`
  color: ${(props) => props.theme.primaryText};
  text-align: center;
  text-justify: center;
  margin: auto;
  padding-left: 20px;
  padding-right: 20px;
  line-height: 30px;
`;

const NextButton = styled.button`
  width: min(15vw, 80px);
  height: min(10vw, 30px);
  background-color: ${(props) => props.theme.primaryButton};
  border-radius: 10px;
  box-shadow: 3px 3px 12px ${(props) => props.theme.secondaryBackgroundShadow};
  color: ${(props) => props.theme.primaryText};
  justify-items: center;
  align-content: center;
  display: flex;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 20px;
  text-align: center;
  text-justify: center;
  align-items: center;
  justify-content: center;
`;
