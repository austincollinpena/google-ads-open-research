import MuxPlayer from "@mux/mux-player-react";
import React from "react";

type props = {
    videoURL: string
}

export default function App(props: props) {
    console.log("looking for ", props.videoURL)
    return (
        <div>
            <MuxPlayer
                streamType="on-demand"
                playbackId={props.videoURL}
                // playbackId="Nbk1OW301yVMFqLj1QKlHjYVbnTQKqEnlI11rTBuvijQ"
                metadata={{
                    video_id: "Explanation of report",
                    video_title: "Test video title",
                    viewer_user_id: "public",
                }}
            />

        </div>

    );
}
