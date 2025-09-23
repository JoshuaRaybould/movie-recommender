import { Link } from "react-router-dom";

type Token = {
  userToken: string;
};
const NavBar = ({ userToken }: Token) => {
  return (
    <div>
      <ul>
        <Link to={`/${userToken}`}>
          <li className="inline-block">Home</li>
        </Link>
        {userToken ? (
          <Link to={`/${userToken}/recommendations`}>
            <li className="inline-block ml-4">Recommendations</li>
          </Link>
        ) : (
          <Link to="/">
            <li className="inline-block ml-4">Recommendations</li>
          </Link>
        )}

        <Link to="/">
          <li className="inline-block ml-4">Sign in</li>
        </Link>
      </ul>
    </div>
  );
};

export default NavBar;
