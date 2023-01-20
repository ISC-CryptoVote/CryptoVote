import { Component } from '@angular/core';
import { Router } from '@angular/router';
import jwt_decode from 'jwt-decode';
import { ApiCallsService } from 'src/app/services/api-calls.service';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent {

  loggedid: string = "";
  devoced_token: JWTContent;
  users: JSON[] = [];

  constructor(private router: Router, private apiservice: ApiCallsService) {
    this.devoced_token = jwt_decode<JWTContent>(localStorage.getItem("JWT") || "{}");
    console.log(this.devoced_token)
    this.loggedid = "Logged in to system as " + this.devoced_token.username + " representing " + this.devoced_token.gnDivision + " division"
    this.onpendingtabselected()
  }

  gotohome(): void {
    console.log("Loading Home Page")
    const navigationDetails: string[] = ['/'];
    this.router.navigate(navigationDetails);
  }

  onaccepttabselected(): void {
    console.log("CLICKED ACCEPTED ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (verifiedSign(content, signature)) {
        res.content.forEach((user: any) => {
          if (user.status == "Approved") {
            console.log(user.status)
            this.users.push(user)
          }
        });
      }
      else {
        throw new Error("invalid Signature")
      }
    }, (err: any) => {
      console.log(err)
    });

  }
  onpendingtabselected(): void {
    console.log("CLICKED PENDING ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (verifiedSign(content, signature)) {
        res.content.forEach((user: any) => {
          if (user.status == "Pending") {
            console.log(user.status)
            this.users.push(user)
          }
        });
      }
      else {
        throw new Error("invalid Signature")
      }
    }, (err: any) => {
      console.log(err)
    });
  }
  onrejecttabselected(): void {
    console.log("CLICKED REJECTED ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (verifiedSign(content, signature)) {
        res.content.forEach((user: any) => {
          if (user.status == "Rejected") {
            console.log(user.status)
            this.users.push(user)
          }
        });
      }
      else {
        throw new Error("invalid Signature")
      }
    }, (err: any) => {
      console.log(err)
    });
  }

}

interface JWTContent {
  aud: string
  exp: number
  gnDivision: string
  iat: number
  id: string
  iss: string
  sub: string
  username: string
}

function verifiedSign(content: any, signature: any): boolean {
  // PK NEED TO GET FROM CA
  
  return true
}
