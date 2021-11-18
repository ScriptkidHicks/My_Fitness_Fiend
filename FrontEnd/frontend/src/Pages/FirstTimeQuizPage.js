import jwtDecode from "jwt-decode";
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

import blob from "../Images/MonsterImages/blobGuy1.png";
import aqua from "../Images/MonsterImages/aquaGuy1.png";

// this is the first time quiz page. It will be gated by both login status, and whether they have completed the first time quiz. If they have then we will send them back to the monster main page. There will also be no ribbon bar on this page, to prevent them from manually
function FirstTimeQuizPage() {
  const [monsterImage, setMonsterImage] = useState(null);
  const theme = useContext(ColorContext);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  let usertoken = jwtDecode(localStorage.getItem("id_token"));
  let user_id = usertoken.user_id;

  const [species, setSepecies] = useState(null);
  const [experience, setExperience] = useState(null);
  const [daysPerWeek, setDaysPerWeek] = useState(null);
  const [availableEquipment, setAvailableEquipment] = useState(null);

  const [modalIndex, setModalIndex] = useState(0);

  function incrementIndex() {
    setModalIndex(modalIndex + 1);
  }

  function decrementIndex() {
    setModalIndex(modalIndex - 1);
  }

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

  function DisplayNewMonster(image) {
    setMonsterImage(image);
  }

  function SubmitResults() {
    const quizResults = {
      method: "PUT",
      headers: { "Content-Type": "application/json", Contents: "request" },
      body: JSON.stringify({
        species: species,
        experience: experience,
        daysPerWeek: daysPerWeek,
        availableEquipment: availableEquipment,
      }),
    };

    fetch("/submit_user_quiz", quizResults).then((response) => {
      if (response.status === 201) {
        navigate("/MonsterPage");
      }
    });
  }

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
        {modalIndex === 0 ? (
          <QuizSection theme={theme}>
            <IntroductionText>
              Welcome to the first time quiz! We'll gather some information
              about what your workout life looks like, and what monster is right
              for you!
            </IntroductionText>
            <IndexButton theme={theme} onClick={incrementIndex}>
              Take Quiz
            </IndexButton>
          </QuizSection>
        ) : null}
        {modalIndex === 1 ? (
          <QuizSection theme={theme}>
            <IntroductionText theme={theme}>
              Which Monster would you like?
            </IntroductionText>
            <MonsterImageDisplay
              monsterImage={monsterImage}
            ></MonsterImageDisplay>
            <LateralSelectWrapper>
              <MonsterSelectButton
                theme={theme}
                onClick={() => {
                  DisplayNewMonster(aqua);
                  setSepecies("aqua");
                }}
              >
                Acquatic
              </MonsterSelectButton>
              <MonsterSelectButton
                theme={theme}
                onClick={() => {
                  DisplayNewMonster(blob);
                  setSepecies("blob");
                }}
              >
                Goo
              </MonsterSelectButton>
            </LateralSelectWrapper>
            <LateralSelectWrapper>
              <IndexButton theme={theme} onClick={decrementIndex}>
                Previous
              </IndexButton>
              <IndexButton
                theme={theme}
                onClick={() => {
                  if (species !== null) {
                    incrementIndex();
                  }
                }}
              >
                Next
              </IndexButton>
            </LateralSelectWrapper>
          </QuizSection>
        ) : null}
        {modalIndex === 2 ? (
          <QuizSection theme={theme}>
            <IntroductionText theme={theme}>
              How much experience do you have?
            </IntroductionText>
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setExperience("None")} />{" "}
              None
            </RadioWrapper>
            <RadioWrapper>
              <RadioInput
                type="radio"
                onClick={() => setExperience("beginner")}
              />{" "}
              Beginner
            </RadioWrapper>
            <RadioWrapper>
              <RadioInput
                type="radio"
                onClick={() => setExperience("Intermediate")}
              />
              Intermediate
            </RadioWrapper>
            <RadioWrapper style={{ paddingBottom: "50px" }}>
              <RadioInput
                type="radio"
                onClick={() => setExperience("advanced")}
              />
              Advanced
            </RadioWrapper>
            <LateralSelectWrapper>
              <IndexButton theme={theme} onClick={decrementIndex}>
                Previous
              </IndexButton>
              <IndexButton
                theme={theme}
                onClick={() => {
                  if (experience !== null) {
                    incrementIndex();
                  }
                }}
              >
                Next
              </IndexButton>
            </LateralSelectWrapper>
          </QuizSection>
        ) : null}
        {modalIndex === 3 ? (
          <QuizSection theme={theme}>
            <IntroductionText theme={theme}>
              How many Days a week do you plan to work out?
            </IntroductionText>
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(1)} /> 1
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(2)} /> 2
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(3)} /> 3
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(4)} /> 4
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(5)} /> 5
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(6)} /> 6
            </RadioWrapper>{" "}
            <RadioWrapper style={{ paddingBottom: "50px" }}>
              <RadioInput type="radio" onClick={() => setDaysPerWeek(7)} /> 7
            </RadioWrapper>
            <LateralSelectWrapper>
              <IndexButton theme={theme} onClick={decrementIndex}>
                Previous
              </IndexButton>
              <IndexButton
                theme={theme}
                onClick={() => {
                  if (daysPerWeek !== null) {
                    incrementIndex();
                  }
                }}
              >
                Next
              </IndexButton>
            </LateralSelectWrapper>
          </QuizSection>
        ) : null}
        {modalIndex === 4 ? (
          <QuizSection theme={theme}>
            <IntroductionText theme={theme}>
              What kind of equipment do you have available?
            </IntroductionText>
            <RadioWrapper>
              <RadioInput
                type="radio"
                onClick={() => setAvailableEquipment("dumbells")}
              />{" "}
              Dumbells
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput
                type="radio"
                onClick={() => setAvailableEquipment("barbells")}
              />{" "}
              Barbells
            </RadioWrapper>{" "}
            <RadioWrapper>
              <RadioInput
                type="radio"
                onClick={() => setAvailableEquipment("both")}
              />{" "}
              Both
            </RadioWrapper>{" "}
            <RadioWrapper style={{ paddingBottom: "50px" }}>
              <RadioInput
                type="radio"
                onClick={() => setAvailableEquipment("None")}
              />{" "}
              None
            </RadioWrapper>
            <LateralSelectWrapper>
              <IndexButton theme={theme} onClick={decrementIndex}>
                Previous
              </IndexButton>
              <IndexButton
                theme={theme}
                onClick={() => {
                  if (availableEquipment !== null) {
                    SubmitResults();
                  }
                }}
              >
                Submit
              </IndexButton>
            </LateralSelectWrapper>
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
  align-items: center;
  height: 60vh;
  width: min(80vw, 600px);
  background-color: ${(props) => props.theme.secondaryBackground};
  box-shadow: -8px 8px 20px ${(props) => props.theme.secondaryBackgroundShadow};
  border-radius: 20px;
`;

const IntroductionText = styled.h3`
  flex-grow: 2;
  padding-top: 40px;
  color: ${(props) => props.theme.primaryText};
  text-align: center;
  text-justify: center;
  margin: auto;
  padding-bottom: 0;
  padding-left: 20px;
  padding-right: 20px;
  line-height: 30px;
`;

const IndexButton = styled.button`
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

const MonsterSelectButton = styled.button`
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

const LateralSelectWrapper = styled.div`
  flex-grow: 2;
  display: flex;
  flex-direction: row;
  justify-content: space-space-evenly;
  align-items: center;
  width: 80%;
  margin-top: 20px;
  margin-bottom: 20px;
  padding-left: 20px;
  padding-right: 20px;
`;

const MonsterImageDisplay = styled.div`
  background: url(${(props) => props.monsterImage});
  background-size: contain;
  background-position: center;
  width: min(30vw, 500px);
  height: min(30vw, 500px);
  border-radius: 20px;
  overflow: hidden;
  background-repeat: no-repeat;
`;

const RadioInput = styled.input`
  padding-top: 20px;
  padding-bottom: 50px;
`;
const RadioWrapper = styled.div`
  flex-grow: 1;
  width: 100%;
  justify-content: center;
  align-items: center;
  display: flex;
`;
