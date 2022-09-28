import { CheckAuthResponse } from "../../go-types";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useEffect } from "react";

type HookResponse = {
  Loading: boolean;
  Data: CheckAuthResponse | undefined;
  Error: string;
};

export default function checkAuth() {
  const fetchCheckAuth = (): Promise<CheckAuthResponse> => {
    axios.defaults.withCredentials = true;
    return axios
      .get(`${import.meta.env.PUBLIC_PUBLIC_API}/v1/api/user/check-auth`)
      .then((res) => {
        return res.data as unknown as CheckAuthResponse;
      });
  };

  const { isLoading, error, data, isFetching } = useQuery(
    ["auth"],
    fetchCheckAuth,
    {
      refetchInterval: 5000, // 5 second polling
    }
  );

  useEffect(() => {
    console.log(data);
  }, [data]);

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>error....</p>;
  }
  if (data && data.isValid === false) {
    return (
      <div>
        <a
          href={`${import.meta.env.PUBLIC_PUBLIC_API}/v1/api/oauth/auth?state=${
            window.location.href
          }`}
          className="underline"
        >
          Authenticate With Google
        </a>
      </div>
    );
  }
  if (data) {
    return (
      <>
        <p>email is: {data.email}</p>
        <p>
          You are authenticated for the next:{" "}
          {Math.floor(data.timeLeftInSeconds / 60)} minutes
        </p>
      </>
    );
  }
  return <p>No data</p>;
}
