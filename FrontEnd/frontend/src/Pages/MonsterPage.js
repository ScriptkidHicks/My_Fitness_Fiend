import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import jwtDecode from "jwt-decode";

// the following are the images we use for monsters
import Aqua1 from "../Images/MonsterImages/aquaGuy1.png";
import Aqua2 from "../Images/MonsterImages/aquaGuy2.png";
import Aqua3 from "../Images/MonsterImages/aquaGuy3.png";
import Blob1 from "../Images/MonsterImages/blobGuy1.png";
import Blob2 from "../Images/MonsterImages/blobGuy2.png";
import Blob3 from "../Images/MonsterImages/blobGuy3.png";
import Blob4 from "../Images/MonsterImages/blobGuy4.png";
import Kettle1 from "../Images/MonsterImages/kettle1.png";
import Kettle2 from "../Images/MonsterImages/kettle2.png";
import Kettle3 from "../Images/MonsterImages/kettle3.png";
import Kettle4 from "../Images/MonsterImages/kettle4.png";

import RibbonBar from "../Components/RibbonBar";

function MonsterPage() {
  // this is used to force user navigation between pages
  const navigate = useNavigate();
  const theme = useContext(ColorContext);
  const [loading, setLoading] = useState(true);
  const [monsterName, setMonsterName] = useState(null);
  // eventually this state will be used to track the fulness of the exp bar.
  const [exp, setExp] = useState(null);
  const [monsterType, setMonsterType] = useState(null);
  const [level, setLevel] = useState(null);
  const [monsterImage, setMonsterImage] = useState(null);

  const [descriptor, setDescriptor] = useState(null); //this is what we're going to use for now to handle descriptions of the monster. Eventually I would love to have this live in the backend and be passed forward.

  // this function needs to be fixed, and the monster images we're storing need to be changed to reflect the two monster lineages that are currently being offered.
  function ImageSourceChanger() {
    if (monsterType === "Aqua") {
      setDescriptor(
        "The Aqua always has a positive attitude, and energy to tackle the day. Aquas are here to believe in you, and your ability to accomplish your goals, even if that doesn't happen in the time frame you first set out. They know that the journey matters more than the destination."
      );
      if (level <= 5) {
        setMonsterImage(Aqua1);
      } else if (level <= 10) {
        setMonsterImage(Aqua2);
      } else {
        setMonsterImage(Aqua3);
      }
    } else if (monsterType === "Blob") {
      setDescriptor(
        "The Blob is a small, but affectionate, monster. It believes in your abliity to tackle each workout, even if you don't complete it in one go. Blobs know that the most important step any of us can take is the next step."
      );
      if (level <= 5) {
        setMonsterImage(Blob1);
      } else if (level <= 10) {
        setMonsterImage(Blob2);
      } else if (level <= 15) {
        setMonsterImage(Blob3);
      } else {
        setMonsterImage(Blob4);
      }
    } else if (monsterType === "Kettle Hell") {
      setDescriptor(
        "Kettle Hell is a tough little monster. It knows that often getting through the day, or a workout, is a matter of endurance. It knows that you have what it takes to get through this workout, and that you'll be stronger for it."
      );
      if (level <= 5) {
        setMonsterImage(Kettle1);
      } else if (level <= 10) {
        setMonsterImage(Kettle2);
      } else if (level <= 15) {
        setMonsterImage(Kettle3);
      } else {
        setMonsterImage(Kettle4);
      }
      //error handle
    }
  }

  // this is how we determine if the user is logged in or not. Syntax may need to become asynchronous if loading times become an issue.
  useEffect(() => {
    let userToken = localStorage.getItem("id_token");
    if (userToken !== undefined && userToken !== null) {
      // be sure to gate decoding behind a check. This allows for graceful navigation.
      userToken = jwtDecode(userToken);
    }
    if (userToken === undefined || userToken === null) {
      navigate("/SignIn");
    } else {
      if (userToken.exp * 1000 < Date.now()) {
        navigate("/SignIn");
      } else {
        let user_id = userToken.user_id;
        const monsterFetch = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            user_token: user_id,
          },
        };
        fetch("/get_user_info", monsterFetch)
          .then((response) => {
            if (response.status !== 201) {
              return null;
            } else {
              return response.json();
            }
          })
          .then((json) => {
            if (json === null) {
              navigate("/signin");
            } else {
              console.log(json);
              if (json.has_finished_quiz === 0) {
                navigate("/FirstTimeQuizPage");
              } else {
                setMonsterName(json.name ? json.name : json.species);
                setMonsterType(json.species);
                setExp(parseInt(json.exp) * 100);
                setLevel(json.level);
                setLoading(false);
                ImageSourceChanger();
              }
            }
          });
      }
    }
  });

  // these consts are fed to the ribbon bar. Be sure that they are ordered in the same way for both targets and titles.
  const pageTargets = ["/AccountPage", "/WorkoutLogPage", "/PastWorkoutsPage"];
  const pageTitles = [
    "Your Account Info",
    "Daily Workout Log",
    "Your Past Workouts",
  ];

  if (loading) {
    // this upper div is returned to the user and rendered until the loading is finished
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
        <RibbonBar pageTargets={pageTargets} pageTitles={pageTitles} />
        <MonsterPageWrapper>
          <XPBar>
            <XPSlider exp={exp} />
          </XPBar>
          <MonsterNameWrapper>
            <MonsterName>
              {monsterName}, Level: {level}
            </MonsterName>
          </MonsterNameWrapper>
          <MonsterImageWrapper
            monsterImage={monsterImage}
          ></MonsterImageWrapper>
          <BottomContentWrapper>
            <MonsterInfo>{descriptor}</MonsterInfo>
          </BottomContentWrapper>
          {/* Level up button has been removed for the time being. Testing with it has been completed, and it is no longer needed. */}
        </MonsterPageWrapper>
      </Body>
    );
  }
}

export default MonsterPage;

const Body = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
`;

const MonsterPageWrapper = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
  overflow: hidden;
`;

const XPBar = styled.div`
  border: solid black 4px;
  border-radius: 12px;
  height: min(10vh, 40px);
  width: min(98%, 700px);
`;

const XPSlider = styled.div`
  height: ${(props) => props.exp}%;
  width: 45%;
  height: min(10vh, 40px);
  background-color: green;
  border-radius: 12px;
`;

const MonsterNameWrapper = styled.div`
  width: min(90%, 600px);
  flex-grow: 0.1;
  display: flex;
  flex-direction: row-reverse;
  justify-content: flex-start;
`;

const MonsterName = styled.h2`
  line-height: 100%;
`;

const MonsterImageWrapper = styled.div`
  background: url(${(props) => props.monsterImage});
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
  width: min(70vw, 400px);
  height: min(70vw, 400px);
  border-radius: 20px;
  overflow: hidden;
`;

const BottomContentWrapper = styled.div`
  width: min(100%, 800px);
  flex-grow: 2;
  text-align: center;
  text-justify: center;
`;

const MonsterInfo = styled.p`
  font-size: max(3vmin, 12pt);
  padding-left: 20px;
  padding-right: 20px;
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

// Im keeping this around for further testing, but currently the need for this visual element has deprecated. It was used for testing that our leveling function worked correctly.
const LevelupButton = styled.button`
  color: ${(props) => props.theme.primaryText};
  background-color: ${(props) => props.theme.secondaryButton};
  width: min(80%, 130px);
  height: 10%;
  border-radius: 10px;
  text-align: center;
  text-justify: center;
  margin-top: 12vh;
  transition: ease all 0.2s;

  :hover {
    background-color: ${(props) => props.theme.secondaryButtonHover};
  }
`;
