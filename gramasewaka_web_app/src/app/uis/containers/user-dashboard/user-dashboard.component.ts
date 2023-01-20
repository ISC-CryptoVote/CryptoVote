import { Component } from '@angular/core';
import { Router } from '@angular/router';
import jwt_decode from 'jwt-decode';
import { ApiCallsService } from 'src/app/services/api-calls.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent {

  loggedid: string = "";
  devoced_token: JWTContent;
  users: User[] = [];
  sel:string=""

  constructor(private router: Router, private apiservice: ApiCallsService, private http: HttpClient) {
    this.devoced_token = jwt_decode<JWTContent>(localStorage.getItem("JWT") || "{}");
    console.log(this.devoced_token)
    this.loggedid = "Logged in to system as " + this.devoced_token.username + " representing " + this.devoced_token.gnDivision + " division"
    this.onpendingtabselected()
    this.sel="Pending"
  }

  gotohome(): void {
    console.log("Loading Home Page")
    const navigationDetails: string[] = ['/'];
    this.router.navigate(navigationDetails);
  }

  onaccepttabselected(): void {
    this.users=[]
    this.sel="Accepted"
    console.log("CLICKED ACCEPTED ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (this.verifiedSign(content, signature)) {
        res.content.forEach((user: any) => {
          if (user.status == "Approved") {
            console.log(user.status)
            this.users.push(user)
          }
        });
        console.log(this.users)
      }
      else {
        throw new Error("invalid Signature")
      }
    }, (err: any) => {
      console.log(err)
    });

  }
  onpendingtabselected(): void {
    this.users=[]
    this.sel="Pending"
    console.log("CLICKED PENDING ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (this.verifiedSign(content, signature)) {
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
    this.users=[]
    this.sel="Rejected"
    console.log("CLICKED REJECTED ")
    this.apiservice.getusers().subscribe((res: any) => {
      let content = res.content
      let signature = res.signature
      if (this.verifiedSign(content, signature)) {
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
  verifiedSign(content: any, signature: any): boolean {
    // PUBLIC KEY NEED TO GET FROM CA
    this.http.get("assets/key_pair/ca/public.pem", { responseType: 'text' as 'json' }).subscribe((key) => {
      console.log(key);
      const crypto = require('crypto');
      const isverified = crypto.verify("SHA256", content, key.toString(), signature);
      console.log(isverified)
      return isverified
    })
    return true
  }

  updateStatus(nic:string,status:string){
    this.users.forEach((user: User) => {
      if (user.nic == nic) {
        user.status=status
        const payload={"nic":nic,"status":status}
        const sign=this.SignPayload(payload)
        this.apiservice.updatevoter(payload,sign)
      }
    });
    console.log(this.users)
  }

  SignPayload(payload: { nic: string; status: string; }) {
    // SHOULD SIGN WITH PVT KEY
    return ""
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

interface User {
  address: string
  gnDivision: string
  id: number
  macHash: string
  name: string
  nic: string
  phone: string
  pubKey: string
  status: string
}



