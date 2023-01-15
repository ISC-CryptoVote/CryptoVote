import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-container',
  templateUrl: './login-container.component.html',
  styleUrls: ['./login-container.component.css']
})
export class LoginContainerComponent {
  username: string = "";
  password: string = "";
  show: boolean = false;

  constructor(private router: Router){}

  gotohome(): void {
    console.log("Loading Home Page")
    const navigationDetails: string[] = ['/'];
    this.router.navigate(navigationDetails);
  }

  submit() {
    console.log("user name is " + this.username)
    this.clear();
  }
  clear() {
    this.username = "";
    this.password = "";
    this.show = true;
  }
}
