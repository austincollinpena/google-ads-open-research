import ReactQueryProvider from "./reactQueryProvider";
import CheckAuth from "./checkAuth";

export default function ImproperNegativeFinder() {
  return (
    <ReactQueryProvider>
      <NegativeFinder />
    </ReactQueryProvider>
  );
}

const NegativeFinder = () => {
  return (
    <div>
      <CheckAuth />
    </div>
  );
};
