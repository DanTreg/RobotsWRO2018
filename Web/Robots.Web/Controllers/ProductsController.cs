using System;
using System.Web.Mvc;
using ASP.NET_MVC_Application.Extensions;
using ASP.NET_MVC_Application.Models;

namespace ASP.NET_MVC_Application.Controllers
{
    using Newtonsoft.Json;
    using Repositories;
    using System.Linq;

    public class ProductsController : Controller
    {
        private ProductsV2Controller _productsV2Controller = new ProductsV2Controller();
        private ProductBlockchainRepository _productBlockchainRepository = new Repositories.ProductBlockchainRepository();
        private ProductRepository _productRepository = new ProductRepository();
        private RobotRepository _robotRepository = new RobotRepository();
        private MachinesRepository _machinesRepository = new MachinesRepository();

        // получение списка продуктов для ЮАЙ
        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Index()
        {
            // Load the data for the client
            var products = _productsV2Controller.List();
            var model = BuildMainModel();
            model.IsPartial = false;
            // Return the view.
            return View(model);
        }

        public PartialViewResult Partial()
        {
            var model = BuildMainModel();
            model.IsPartial = true;

            return PartialView("Index", model);
        }

        public MainModel BuildMainModel()
        {
            var robots = _robotRepository.GetAll();
            var robot1 = robots[0];
            var robot2 = robots[1];

            var products = _productRepository.GetAll();
            var productBlockchains = _productBlockchainRepository.GetAll();

            var model = new MainModel();
            foreach (var item in products)
            {
                var productModel = new ProductModel
                {
                    Destination = item.Destination,
                    ExpirationDate = item.ExpirationDate,
                    ExpirationStatus = item.ExpirationStatus,
                    Id = item.Id,
                    IsDeleted = item.IsDeleted,
                    Name = item.Name,
                    Place = item.Place,
                    Reason = item.Reason,
                    Supplier = item.Supplier
                };

                productModel.ProductBlockchains.AddRange(productBlockchains);
                model.Products.Add(productModel);
            }

            var robot1Product = products.FirstOrDefault(x => x.Place == Place.InTransportation1);
            if (robot1Product != null)
            {
                ProductModel product = JsonConvert.DeserializeObject<ProductModel>(JsonConvert.SerializeObject(robot1Product));

                product.ProductBlockchains = productBlockchains.Where(x => x.ProductId == product.Id).ToList();

                model.Robot1 = new RobotModel
                {
                    Id = robot1.Id,
                    Direction = robot1.Direction,
                    IsDeleted = robot1.IsDeleted,
                    Name = robot1.Name,
                    Product = product
                };
            }

            var robot2Product = products.FirstOrDefault(x => x.Place == Place.InTransportation2);

            if (robot2Product != null)
            {
                ProductModel product = JsonConvert.DeserializeObject<ProductModel>(JsonConvert.SerializeObject(robot2Product));
                product.ProductBlockchains = productBlockchains.Where(x => x.ProductId == product.Id).ToList();


                model.Robot2 = new RobotModel
                {
                    Id = robot2.Id,
                    Direction = robot2.Direction,
                    IsDeleted = robot2.IsDeleted,
                    Name = robot2.Name,
                    Product = product
                };
            }

            var machine = _machinesRepository.GetAll().FirstOrDefault();
            if (machine != null)
            {
                model.MachineIncome = machine.MachineIncome;
                model.MachineOutcome = machine.MachineOutcome;
                model.MachineUtilization = machine.MachineUtilization;
            }
            return model;
        }

        //Создание продукта для ЮАЙ
        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Create()
        {
            var all = _productsV2Controller.List();
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
                var supplier = Request.Form["supplier"];
                var placeinstorage = Request.Form["Place"];
                //var expirationstatus = 1;
                var place = Request.Form["place"];
                DateTime expirationdate = Convert.ToDateTime(Request.Form["expirationdate"]);

                var expirationstatus = SetExpirationStatus(id, expirationdate);

                // Create a new Client for these details.
                Product product = new Product()
                {
                    Name = name,
                    Supplier = supplier,
                    ExpirationDate = expirationdate.Date,
                    Place = (Place)Enum.Parse(typeof(Place), place),
                    ExpirationStatus = expirationstatus.ExpirationStatus,
                    Reason = expirationstatus.Reason
                };
                _productsV2Controller.Create(product);

                // Save the client in the ClientList


                // Denote that the client was created
                created = true;
            }

            if (created)
            {
                ViewBag.Message = "Создан Контракт на размещение продукта " + Request.Form["name"];
            }
            else
            {
                ViewBag.Message = "There was an error while creating the client.";
            }
            return View();
        }


        //Обновление продукта для ЮАЙ
        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Update(int id)
        {
            var all = _productsV2Controller.List();
            ViewBag.All = all;

            if (HttpContext.Request.RequestType == "POST")
            {
                // Request is Post type; must be a submit
                var name = Request.Form["name"];
                var supplier = Request.Form["supplier"];
                var place = Request.Form["Place"];
                //var expirationstatus = 1;
                DateTime expirationdate = Convert.ToDateTime(Request.Form["expirationdate"]);
                // Get all of the clients

                var product = _productsV2Controller.GetById(id);

                // Find the product
                // product found, now update his properties and save it.
                var expirationstatus = SetExpirationStatus(id, expirationdate);
                product.Name = name;
                product.Supplier = supplier;
                product.ExpirationDate = expirationdate;
                product.ExpirationStatus = expirationstatus.ExpirationStatus;
                product.Reason = expirationstatus.Reason;
                product.Place = (Place)Enum.Parse(typeof(Place), place);

                _productsV2Controller.Update(product);

                // Add the details to the View
                Response.Redirect("~/Products/Index?Message=Product_Updated");
            }

            return View(_productsV2Controller.GetById(id));
        }

        //Удаление продукта для ЮАЙ
        [BasicAuthenticationAttribute("robots", "robots", BasicRealm = "robots")]
        public ActionResult Delete(int id)
        {
            var deleted = false;

            var product = _productsV2Controller.GetById(id);
            if (product != null)
            {
                _productsV2Controller.Delete(product);
                deleted = true;
            }

            // Add the process details to the ViewBag
            if (deleted)
            {
                ViewBag.Message = "Продукт успешно удален.";
            }
            else
            {
                ViewBag.Message = "There was an error while deleting the product.";
            }
            return View();
        }

        //Выставление Статуса продукта (для ЮАЙ)
        public ProductUpdateExpirationStatusModel SetExpirationStatus(int ProductId, DateTime ExpirationDate)
        {
            int expirationstatus = 1;
            string reason = "";
            if (DateTime.Now.Date.AddDays(7) < ExpirationDate.Date)
            {
                expirationstatus = 2;
            }

            if ((DateTime.Now.Date < ExpirationDate.Date) && (ExpirationDate.Date < DateTime.Now.Date.AddDays(7)))
            {
                expirationstatus = 3;

            }

            if (DateTime.Now >= ExpirationDate.Date)
            {
                expirationstatus = 4;
                reason = "Просрочено";
            }

            ProductUpdateExpirationStatusModel result = new ProductUpdateExpirationStatusModel();
            result.ExpirationStatus = expirationstatus;
            result.Reason = reason;
            return result;
        }

        //получение данных для стеллажа на сайте
        public PartialViewResult ProductsList()
        {
            var all = _productsV2Controller.List();
            return PartialView("ProductPartial", all);
        }

        //получение данных для списка продуктов на сайте
        public PartialViewResult ProductsTable()
        {
            var all = _productsV2Controller.List();
            return PartialView("ProductsTablePartial", all);
        }



    }
}