import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiCallsService } from 'src/app/services/api-calls.service';

@Component({
  selector: 'app-login-container',
  templateUrl: './login-container.component.html',
  styleUrls: ['./login-container.component.css']
})
export class LoginContainerComponent {
  usernamein: string = "";
  passwordin: string = "";
  msg: string = ""
  show: boolean = false;

  constructor(private router: Router, private apiservice: ApiCallsService) { }

  gotohome(): void {
    console.log("Loading Home Page")
    const navigationDetails: string[] = ['/'];
    this.router.navigate(navigationDetails);
  }

  gotodashboard(): void {
    console.log("Loading Dashboard")
    const navigationDetails: string[] = ['/dashboard'];
    this.router.navigate(navigationDetails);
  }

  submit() {
    this.apiservice.login(this.usernamein, this.passwordin).subscribe((res: any) => {
      console.log(res.token);
      localStorage.setItem("JWT", res.token)
      this.gotodashboard()
    }, (err: any) => {
      this.msg = "Login Failed !!"
      console.log(err);
      this.clear();
    })
  }
  
  clear() {
    this.usernamein = "";
    this.passwordin = "";
    this.show = true;
  }
}
