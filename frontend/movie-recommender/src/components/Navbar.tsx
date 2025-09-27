import { Link } from "react-router-dom";

type navInfo = {
  userToken: string;
  searchFunc: Function;
};
const NavBar = ({ userToken, searchFunc }: navInfo) => {
  return (
    <nav className="flex justify-between items-center bg-[#1b1e21] mb-4 h-16">
      <div>
        <a className="text-4xl text-white ml-10" href={`/${userToken}`}>
          MovRec
        </a>
      </div>
      <div>
        <input
          className="pl-2 rounded-lg outline-solid outline-1 h-8 w-150 bg-gray-100"
          placeholder="Search"
          onChange={(e) => {
            searchFunc(e.target.value);
          }}
        />
      </div>
      <div>
        <ul className="flex">
          <li className="block mr-15">
            <a className="text-white" href={`/${userToken}`}>
              Home
            </a>
          </li>
          {userToken ? (
            <li className="block mr-15">
              <a className="text-white" href={`/${userToken}/recommendations`}>
                Recommendations
              </a>
            </li>
          ) : (
            <li className="block p-1">
              <a className="text-white" href="/">
                Recommendations
              </a>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
