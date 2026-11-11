import { useAuth } from "../auth/authContext";

type navInfo = {
  searchFunc: Function;
};

const NavBar = ({ searchFunc }: navInfo) => {
  const { user } = useAuth();

  return (
    <nav className="flex justify-between items-center bg-nav-background mb-4 h-16">
      <div>
        <a
          className="text-4xl text-main-gold font-title ml-10"
          href={`/movies`}
        >
          NBMovie
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
          <li className="block mr-10">
            <a className="text-white" href={`/movies`}>
              Home
            </a>
          </li>
          {user ? (
            <li className="block mr-5">
              <a className="text-white" href={`/recommendations`}>
                Recommendations
              </a>
            </li>
          ) : (
            <li className="block mr-5">
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
