import jwtDecode from "jwt-decode";
import { useContext, useEffect, useState } from "react";
import { resolvePath, useNavigate } from "react-router";
import styled from "styled-components";
import RibbonBar from "../Components/RibbonBar";
import { ColorContext } from "../ContextProviders/ColorContext";

function WorkoutLogPage() {
  let userToken = localStorage.getItem("id_token");
  let userId;
  const navigate = useNavigate();
  if (userToken) {
    userToken = jwtDecode(userToken);
    userId = userToken.user_id;
    if (userToken.exp * 1000 < Date.now()) {
      navigate("/SignIn");
    }
  } else {
    navigate("/SignIn");
  }
  // this is so we can distribute the color context to the individual components.
  const theme = useContext(ColorContext);
  const [loading, setLoading] = useState(true);
  // page targets and page titles are distributed individually to each page. We don't want a page to have a load button for the page that it is already on. Make sure that the page targets correlate correctly to the page titles. They will be unpacked in the same order.
  const [workoutText, setWorkoutText] = useState([]);
  const pageTargets = ["/AccountPage", "/MonsterPage", "/PastWorkoutsPage"];
  const pageTitles = [
    "Your Account Info",
    "Your Monster",
    "Your Past Workouts",
  ];

  function submitWorkoutLog() {
    const workoutResults = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        user_token: userId,
      },
      body: JSON.stringify({
        hasCompleted: workoutCompleted,
      }),
    };

    fetch("/api/complete_workout", workoutResults)
      .then((response) => {
        if (response.status === 200) {
          navigate("/MonsterPage");
          return null;
        } else {
          console.log(response);
          return response.json();
        }
      })
      .then((json) => {
        console.log(json);
      });
  }

  const [workoutCompleted, setWorkoutCompleted] = useState(false);

  useEffect(() => {
    const workoutFetch = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        user_token: 1,
      },
    };

    fetch("/api/daily_workout_info", workoutFetch)
      .then((response) => {
        if (response.status === 200) {
          return response.text();
        } else {
          return null;
        }
      })
      .then((text) => {
        if (text === null) {
          alert("Whoops, no workout to be provided");
        } else {
          setWorkoutText(
            text.split(",").map((set) => {
              if (set) {
                return <li>{set}</li>;
              }
            })
          );
          setLoading(false);
        }
      });
  }, []);

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
        <RibbonBar pageTitles={pageTitles} pageTargets={pageTargets} />
        <WorkoutLogPageWrapper>
          <WorkoutLogWrapper theme={theme}>
            <WorkoutLogTextBox theme={theme}>{workoutText}</WorkoutLogTextBox>
            <SubmitSwitchWrapper>
              <RadioWrapper theme={theme}>
                <RadioInput
                  type="checkbox"
                  onClick={() => {
                    setWorkoutCompleted(!workoutCompleted);
                  }}
                />
                I completed this workout
              </RadioWrapper>
              <SubmitButton theme={theme} onClick={submitWorkoutLog}>
                Submit
              </SubmitButton>
            </SubmitSwitchWrapper>
          </WorkoutLogWrapper>
        </WorkoutLogPageWrapper>
      </Body>
    );
  }
}

export default WorkoutLogPage;

const Body = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: ${(props) => props.theme.primaryBackground};
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

const WorkoutLogWrapper = styled.div`
  background: ${(props) => props.theme.secondaryBackground};
  box-shadow: -8px 8px 20px ${(props) => props.theme.secondaryBackgroundShadow};
  border-radius: 12px;
  height: 70vh;
  width: min(80vw, 500px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const WorkoutLogTextBox = styled.p`
  background: ${(props) => props.theme.secondaryTextBackground};
  border-radius: 10px;
  width: 75%;
  flex-grow: 1;
  padding: 20px;
  color: ${(props) => props.theme.primaryText};
  line-height: 2;
  margin-bottom: 0;
  margin-top: 3vh;
  font-size: 2vh;
`;

const WorkoutLogPageWrapper = styled.div`
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
`;

const SubmitButton = styled.button`
  background-color: ${(props) => props.theme.primaryButton};
  color: ${(props) => props.theme.primaryText};
  border-radius: 16px;
  border: 3px solid ${(props) => props.theme.primaryButtonOutline};
  transition: ease all 0.2s;
  font-size: 2.5vh;
  font-weight: bold;
  height: min(70%, 70px);
  padding-left: 20px;
  padding-right: 20px;
  margin: auto;
  margin-right: 4vw;

  :hover {
    box-shadow: -3px 3px 6px ${(props) => props.theme.secondaryBackgroundShadow};
    border: 3px solid ${(props) => props.theme.primaryButtonHoverOutline};
  }
`;

const SubmitSwitchWrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  height: 25%;
  padding: 10px;
`;

const RadioInput = styled.input`
  margin: 20px;
  height: 20px;
  width: 20px;
`;

const RadioWrapper = styled.div`
  padding: auto;
  margin: auto;
  color: ${(props) => props.theme.primaryText};
  background: none;
  justify-content: center;
  align-items: center;
  display: flex;
`;
