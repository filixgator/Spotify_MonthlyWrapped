# About

**Gatorfy** uses the **Spotify Web API** for a personal application that makes small quality of life improvements.
> Currently not open to the public

# Features
- User's authorization as required by the Spotify Web API.
- User's top items data retreival.
- Playlist creation on behalf of the user.

## Implementation

### Frontend

Gatorfy's frontend is hosted using **Google's Firebase** platform, and uses **Bootstrap** and **React** to display it's home page. This is a single-page React proyect that introduces Gatorfy to the user, and provides a description of it's the current functionality and the option to try them out.

![Home Page for Gatorfy](https://github.com/filixgator/Spotify_MonthlyWrapped/blob/main/Media/HomePage.PNG?raw=true "Home Page")

The first time the user selects an option, they will be redirected to the Spotify log in page, for authentication and to authorize Gatorfy to request information from their Spotify profile.

Once Gatorfy ends with the backend operations, the page will preview the name of the created playlist, and gives the opportunity to try another feature.

### Backend

Gatorfy is currently using the **AWS Lambda** and **AWS API Gateway** services to execute all of the backend operations. After receiveing authorization from the end user, Gatorfy uses simple REST principles to request JSON metadata from the Spotify Web API endpoints, which includes data from the user and from the Spotify Data Catalogue. Once the requested data is received, Gatorfy creates a playlist and adds the appropiate tracks, this playlist will be found on the user's Library.
