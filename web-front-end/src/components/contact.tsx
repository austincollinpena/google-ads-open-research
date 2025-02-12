import { EnvelopeIcon, PhoneIcon } from "@heroicons/react/24/outline/index.js";
import { useState, useRef } from "react";

export type Props = {
  Headline: string;
  Description: string;
  FormPlaceholder: string;
  ButtonText: string;
};

export default function Contact(props: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [formSuccess, setFormSuccess] = useState(false);
  const formRef = useRef<null | HTMLFormElement>(null);

  const submit = (e: any) => {
    e.preventDefault();

    const valid = formRef.current?.reportValidity();

    if (!valid) {
      return;
    }

    const formObject = {
      name: name,
      email: email,
      message: message,
    };

    // @ts-ignore
    const formBody: any = Object.keys(formObject)
      .map(
        (key) =>
          // @ts-ignore
          encodeURIComponent(key) + "=" + encodeURIComponent(formObject[key])
      )
      .join("&");

    fetch("https://form-email.easylanding.io/google-ads-open-research", {
      method: "Post",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      },
      body: formBody,
    })
      .catch((e) => {
        window.alert("form submission failed, email me directly");
      })
      .finally(() => {
        setName("");
        setEmail("");
        setMessage("");
        setFormSuccess(true);
      });
    return;
  };

  return (
    <div className="relative bg-brandNeutral">
      <div className="absolute inset-0">
        <div className="absolute inset-y-0 left-0 w-1/2 bg-brandNeutral" />
      </div>
      <div className="relative mx-auto max-w-7xl lg:grid lg:grid-cols-5">
        <div className="bg-brandNeutral py-16 px-4 sm:px-6 lg:col-span-2 lg:px-8 lg:py-24 xl:pr-12">
          <div className="mx-auto max-w-lg">
            <h2 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
              {props.Headline}
            </h2>
            <p className="mt-3 text-lg leading-6 text-gray-500">
              {props.Description}
            </p>
            <dl className="mt-8 text-base text-gray-500">
              <div className="mt-3">
                <dt className="sr-only">Email</dt>
                <dd className="flex">
                  <EnvelopeIcon
                    className="h-6 w-6 flex-shrink-0 text-gray-400"
                    aria-hidden="true"
                  />
                  <span className="ml-3">me@austinpena.com</span>
                </dd>
              </div>
            </dl>
            <p className="mt-6 text-base text-gray-500">
              Looking for work? We're always looking for killer Google Ads
              specialists.{" "}
              <a href="#" className="font-medium text-gray-700 underline">
                Email Us
              </a>
              .
            </p>
          </div>
        </div>
        {/**
        <div className="bg-white py-16 px-4 sm:px-6 lg:col-span-3 lg:py-24 lg:px-8 xl:pl-12">
          <div className="mx-auto max-w-lg lg:max-w-none">
            <form
              onSubmit={(e) => submit(e)}
              className="grid grid-cols-1 gap-y-6"
            >
              <div>
                <label htmlFor="full-name" className="sr-only">
                  Full name
                </label>
                <input
                  type="text"
                  name="full-name"
                  id="full-name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  autoComplete="name"
                  className="block w-full rounded-md border border-gray-300 py-3 px-4 placeholder-gray-500 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Full name"
                  required
                />
              </div>
              <div>
                <label htmlFor="email" className="sr-only">
                  Email
                </label>
                <input
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  name="email"
                  type="email"
                  autoComplete="email"
                  className="block w-full rounded-md border border-gray-300 py-3 px-4 placeholder-gray-500 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Email"
                  required
                />
              </div>
              <div>
                <label htmlFor="message" className="sr-only">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={4}
                  className="block w-full rounded-md border border-gray-300 py-3 px-4 placeholder-gray-500 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder={props.FormPlaceholder}
                  required
                />
              </div>
              <div>
                <button
                  type="submit"
                  className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-3 px-6 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  {props.ButtonText}
                </button>
              </div>
            </form>
            {formSuccess && (
              <p className="text-xl text-green-700 mt-2">
                Successfully submitted, we'll reach out ASAP
              </p>
            )}
          </div>
        </div>
         **/}
      </div>
    </div>
  );
}
