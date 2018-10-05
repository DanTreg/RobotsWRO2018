using ASP.NET_MVC_Application.Extensions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Mvc;
using ASP.NET_MVC_Application.Repositories;
using ASP.NET_MVC_Application.Models;

namespace ASP.NET_MVC_Application.Controllers
{
    public class RobotsController : Controller
    {
        private RobotRepository _robotRepository = new RobotRepository();

        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Index()
        {
            // Load the data for the client
            var robots = List();

            // Return the view.
            return View(robots);
        }

        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Create()
        {
            var all = List();
            ViewBag.All = all;

            ViewBag.Submitted = false;
            var created = false;
            // Create the Client
            if (HttpContext.Request.RequestType == "POST")
            {
                ViewBag.Submitted = true;
                // If the request is POST, get the values from the form
                var id = Convert.ToInt32(Request.Form["id"]);
                var name = Request.Form["name"];
                var direction = Request.Form["Direction"];
                

                // Create a new Client for these details.
                Robot robot = new Robot()
                {
                    Id = id,
                    Name = name,
                    Direction = direction
                };
                _robotRepository.Create(robot);

                // Save the client in the ClientList


                // Denote that the client was created
                created = true;
            }

            if (created)
            {
                ViewBag.Message = "New Robot has been added to Logisitc Center " + Request.Form["name"];
            }
            else
            {
                ViewBag.Message = "There was an error while creating the client.";
            }
            return View();
        }

        public ActionResult Delete(int id)
        {
            var deleted = false;

            var robot = _robotRepository.GetById(id);
            if (robot != null)
            {
                _robotRepository.Delete(robot);
                deleted = true;
            }

            // Add the process details to the ViewBag
            if (deleted)
            {
                ViewBag.Message = "Robot has been Deleted.";
            }
            else
            {
                ViewBag.Message = "There was an error while deleting the product.";
            }
            return View();
        }

        private object List()
        {
            
            return _robotRepository.GetAll();
        }
    }
}
