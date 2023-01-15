import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent {

  constructor(private router: Router){}

  gotohome(): void {
    console.log("Loading Home Page")
    const navigationDetails: string[] = ['/'];
    this.router.navigate(navigationDetails);
  }

  onaccepttabselected():void{}
  onpendingtabselected():void{}
  onrejecttabselected():void{}

}
