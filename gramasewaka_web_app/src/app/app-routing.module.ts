import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { HomeComponent } from './uis/containers/home/home.component';
import { LoginContainerComponent } from './uis/containers/login-container/login-container.component';
import { UserDashboardComponent } from './uis/containers/user-dashboard/user-dashboard.component';

const routes: Routes = [
  { path: 'login', component: LoginContainerComponent },
  { path: '', component: HomeComponent },
  { path: 'dashboard', component: UserDashboardComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
